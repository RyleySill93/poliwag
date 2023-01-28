import enum
import os
import shutil
from typing import List
import pathlib
from decouple import Config, RepositoryEnv
import inquirer
import time
from inquirer.themes import GreenPassion
from blessed import Terminal
from pynpm import NPMPackage
import boto3
import fire

from .utils import run_terminal_cmd, run_commands_remote
from .file_transfer import run_rsync, run_scp


DIR = pathlib.Path(__file__).parent.absolute()
INFRA_DIR = DIR.parent.absolute()
PROJECT_ROOT_DIR = INFRA_DIR.parent.absolute()
BACKEND_DIR = PROJECT_ROOT_DIR / "backend"

THEME = GreenPassion()
term = Terminal()

PROJECT_NAME = "poliwag"


def get_config() -> dict:
    DOTENV_FILE = PROJECT_ROOT_DIR / ".env"
    env_config = Config(RepositoryEnv(DOTENV_FILE))
    return env_config.repository.data


def get_safe_password(message: str = None) -> str:
    pass1 = get_password(message)
    questions = [inquirer.Password("password", message="confirm password")]
    answer = inquirer.prompt(questions, theme=THEME)
    pass2 = answer["password"]

    if not pass1 == pass2:
        raise ValueError("Passwords not matching!")

    return pass1


def get_password(message: str = None) -> str:
    questions = [inquirer.Password("password", message=message or "enter password")]
    answer = inquirer.prompt(questions, theme=THEME)
    return answer["password"]


def get_new_secret_key() -> str:
    import secrets

    return secrets.token_urlsafe()


class EnvironmentEnum(str, enum.Enum):
    SANDBOX = "SANDBOX"
    PRODUCTION = "PRODUCTION"


def select_deploy_environment() -> EnvironmentEnum:
    environments_choices = [
        (EnvironmentEnum.SANDBOX, EnvironmentEnum.SANDBOX,),
        (EnvironmentEnum.PRODUCTION, EnvironmentEnum.PRODUCTION,)
    ]

    questions = [
        inquirer.List("environment", message="Select environment", choices=environments_choices)
    ]
    answer = inquirer.prompt(questions, theme=THEME)

    return answer['environment']


class CloudfrontService:
    def __init__(self):
        config = get_config()
        self.cf_client = boto3.client(
            "cloudfront",
            aws_access_key_id=config["PROD_AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=config["PROD_AWS_SECRET_ACCESS_KEY"],
            region_name=config["PROD_AWS_REGION_NAME"],
        )

    def list_distributions(self) -> List[dict]:
        response = self.cf_client.list_distributions()
        is_success = response["ResponseMetadata"]["HTTPStatusCode"] == 200
        if not is_success:
            raise Exception("AWS API Error!")

        yield from response['DistributionList']['Items']


    def select_distribution_from_list(self, environment: EnvironmentEnum = EnvironmentEnum.SANDBOX) -> dict:
        distributions = self.list_distributions()
        distribution_choices = []
        distributions_by_id = {}
        for distribution in distributions:
            distributions_by_id[distribution["Id"]] = distribution
            # Comments should hold the correct environment. no tags for some reason
            if environment.value in distribution["Comment"].upper():
                distribution_choices.append(
                    (
                        f'id:{distribution["Id"]} - name:{distribution["Comment"]}',
                        distribution["Id"],
                    )
                )

        questions = [
            inquirer.List("distribution_id", message="Select distribution", choices=distribution_choices)
        ]
        answer = inquirer.prompt(questions, theme=THEME)
        return distributions_by_id[answer["distribution_id"]]


class ServerService:
    def __init__(self):
        config = get_config()
        self.ec2_client = boto3.client(
            "ec2",
            aws_access_key_id=config["PROD_AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=config["PROD_AWS_SECRET_ACCESS_KEY"],
            region_name=config["PROD_AWS_REGION_NAME"],
        )

    def list_servers(self) -> List[dict]:
        response = self.ec2_client.describe_instances()
        is_success = response["ResponseMetadata"]["HTTPStatusCode"] == 200
        if not is_success:
            raise Exception("AWS API Error!")

        for res in response["Reservations"]:
            yield from res["Instances"]

    def select_server_from_list(self, environment: EnvironmentEnum = EnvironmentEnum.SANDBOX) -> dict:
        servers = self.list_servers()
        server_choices = []
        servers_by_id = {}
        for server in servers:
            servers_by_id[server["InstanceId"]] = server
            server_tags = {
                tag["Key"].upper(): tag["Value"].upper() for tag in server["Tags"]
            }
            if server_tags.get("ENVIRONMENT") == environment.value:
                import ipdb; ipdb.set_trace()
                server_choices.append(
                    (
                        f'name:{server_tags.get("NAME", "Unknown")} - env:{server_tags.get("ENVIRONMENT", "Unknown")} -> {server["PublicIpAddress"]}',
                        server["InstanceId"],
                    )
                )

        questions = [
            inquirer.List("server_id", message="Select server", choices=server_choices)
        ]
        answer = inquirer.prompt(questions, theme=THEME)
        return servers_by_id[answer["server_id"]]


def get_ssh_key() -> str:
    questions = [
        inquirer.Path(
            "ssh_key",
            default=pathlib.Path.home() / f".ssh/{PROJECT_NAME}_key",
            message="Path to ssh key",
            exists=True,
            path_type=inquirer.Path.FILE,
        )
    ]
    answer = inquirer.prompt(questions, theme=THEME)
    return answer["ssh_key"]


class Initialize:
    def install_packages(self):
        run_terminal_cmd("sudo apt-get update")
        run_terminal_cmd(
            "sudo apt-get install -y build-essential python3-dev python3-pip python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info nginx postgresql postgresql-client supervisor pass redis"
        )
        run_terminal_cmd("sudo apt-get update")

    def postgres(self):
        config = get_config()
        password = get_safe_password("Enter new password for database user")
        question = [
            inquirer.Confirm(
                "edited_conf",
                message="Did you edit /etc/postgresql/12/main/pg_hba.conf and set `local all postgres trust`?",
            )
        ]
        run_terminal_cmd(f"sudo service postgresql restart")
        answer = inquirer.prompt(question, theme=THEME)
        if not answer["edited_conf"]:
            print(term.red("you should do that first or this command wont work."))

        sql_project_id = PROJECT_NAME.replace("-", "_")
        run_terminal_cmd(
            f"psql -U postgres -c \"CREATE ROLE {sql_project_id} login password '{password}'\""
        )
        run_terminal_cmd(
            f'psql -U postgres -c "ALTER USER {sql_project_id} with SUPERUSER"'
        )
        run_terminal_cmd(f'psql -U postgres -c "CREATE DATABASE {sql_project_id}"')

    def application(self):
        config = get_config()
        print(term.limegreen_on_black("installing python dependencies..."))
        run_terminal_cmd(
            f"cd /var/www/{PROJECT_NAME}/backend && pip3 install -r requirements.txt"
        )

        print(term.limegreen_on_black("running database migrations..."))
        run_terminal_cmd(
            f"cd /var/www/{PROJECT_NAME}/backend && python3 manage.py migrate"
        )
        print(term.limegreen_on_black("Application setup almost finished..."))

        secret_key = get_new_secret_key()
        print(
            term.yellow_on_black(
                "But you are not done!!! Create the superuser"
                " `python3 manage.py createsuperuser`"
                f" And set a secret key: {secret_key}"
            )
        )

    def nginx(self):
        print(term.limegreen_on_black("restarting nginx..."))
        run_terminal_cmd("sudo service nginx restart")

    def supervisor(self):
        print(term.limegreen_on_black("updating supervisor..."))
        run_terminal_cmd("sudo supervisorctl reread")
        run_terminal_cmd("sudo supervisorctl update")


class Deploy:
    def backend(self):
        print(term.limegreen_on_black("Starting backend deploy..."))
        start_time = time.time()
        target_env = select_deploy_environment()

        client = ServerService()
        server = client.select_server_from_list(target_env)
        ip_address = server["PublicIpAddress"]
        ssh_key = get_ssh_key()

        print(term.limegreen_on_black("Pulling latest code..."))
        run_commands_remote(
            ssh_key_name=ssh_key,
            ip_address=ip_address,
            commands=[
                f"cd /var/www/{PROJECT_NAME}",
                # deploy current branch on server
                "git pull origin $(git rev-parse --abbrev-ref HEAD)",
            ],
        )
        print(term.limegreen_on_black("Restarting the application..."))
        run_commands_remote(
            ssh_key_name=ssh_key,
            ip_address=ip_address,
            commands=[f"cd /var/www/{PROJECT_NAME}", "sudo supervisorctl restart all"],
        )
        elapsed_time = time.time() - start_time
        formatted_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
        print(term.limegreen_on_black(f"==========================================="))
        print(
            term.limegreen_on_black(f"Backend deploy completed in -> {formatted_time}!")
        )
        print(term.limegreen_on_black(f"==========================================="))

    def backend_full(self):
        print(term.limegreen_on_black("Starting backend deploy..."))
        start_time = time.time()
        client = ServerService()
        server = client.select_server_from_list()
        ip_address = server["PublicIpAddress"]
        ssh_key = get_ssh_key()

        print(term.limegreen_on_black("Pulling latest code..."))
        run_commands_remote(
            ssh_key_name=ssh_key,
            ip_address=ip_address,
            commands=[
                f"cd /var/www/{PROJECT_NAME}",
                "git pull",
            ],
        )
        print(
            term.limegreen_on_black("Installing requirements and running migrations...")
        )
        run_commands_remote(
            ssh_key_name=ssh_key,
            ip_address=ip_address,
            commands=[
                f"cd /var/www/{PROJECT_NAME}",
                f"source /home/ubuntu/.pyenv/versions/{PROJECT_NAME}/bin/activate",
                "pip install -r requirements.txt",
                "make migrate",
            ],
        )
        print(term.limegreen_on_black("Restarting the application..."))
        run_commands_remote(
            ssh_key_name=ssh_key,
            ip_address=ip_address,
            commands=[f"cd /var/www/{PROJECT_NAME}", "sudo supervisorctl restart all"],
        )

        elapsed_time = time.time() - start_time
        formatted_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
        print(term.limegreen_on_black(f"==========================================="))
        print(
            term.limegreen_on_black(f"Backend deploy completed in -> {formatted_time}!")
        )
        print(term.limegreen_on_black(f"==========================================="))

    def rsync_backend(self):
        print(term.limegreen_on_black("Starting backend deploy..."))
        start_time = time.time()
        client = ServerService()
        server = client.select_server_from_list()
        ip_address = server["PublicIpAddress"]
        ssh_key = get_ssh_key()
        run_rsync(
            ssh_key_name=ssh_key,
            ip_address=ip_address,
            local_directory_path=PROJECT_ROOT_DIR.joinpath("backend"),
            target_directory_path=f"/var/www/{PROJECT_NAME}",
        )
        elapsed_time = time.time() - start_time
        formatted_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
        print(term.limegreen_on_black(f"==========================================="))
        print(
            term.limegreen_on_black(f"Backend deploy completed in -> {formatted_time}!")
        )
        print(term.limegreen_on_black(f"==========================================="))

    def frontend(self):
        print(term.limegreen_on_black("Starting frontend deploy..."))
        config = get_config()
        client = CloudfrontService()
        environment = select_deploy_environment()
        distribution = client.select_distribution_from_list(environment)
        start_time = time.time()

        CLOUDFRONT_DIST_ID = distribution["Id"]

        try:
            shutil.rmtree(PROJECT_ROOT_DIR.joinpath("build").absolute())
        except FileNotFoundError:
            pass

        ENV_API_URL_MAP = {
            EnvironmentEnum.SANDBOX: 'https://api.sandbox.poliwag.com',
            EnvironmentEnum.PRODUCTION: 'https://api.poliwag.com',
        }

        ENV_S3_BUCKET_MAP = {
            EnvironmentEnum.SANDBOX: 'poliwag-sandbox-fe',
            EnvironmentEnum.PRODUCTION: 'poliwag-prod-fe',
        }

        api_url = ENV_API_URL_MAP[environment]
        build_command = f"DISABLE_ESLINT_PLUGIN='true' TSC_COMPILE_ON_ERROR=true CI=false REACT_APP_API_URL={api_url} REACT_APP_ENVIRONMENT={environment.value} REACT_APP_GOOGLE=AIzaSyADGC3D0BYoZIvbiZzxfqIa_cNqcq91RE0 REACT_APP_PERSONA_ENVIRONMENT={environment.value.lower()} yarn build"
        print(term.limegreen_on_black("Building frontend..."))
        run_terminal_cmd(build_command)

        print(term.limegreen_on_black("Syncing frontend to S3..."))
        bucket = ENV_S3_BUCKET_MAP[environment]
        run_terminal_cmd(
            f'AWS_ACCESS_KEY_ID={config["PROD_AWS_ACCESS_KEY_ID"]} AWS_SECRET_ACCESS_KEY={config["PROD_AWS_SECRET_ACCESS_KEY"]} aws s3 sync {PROJECT_ROOT_DIR.joinpath("build")} s3://{bucket}'
        )

        print(term.limegreen_on_black("Invalidating cloudfront cache..."))
        run_terminal_cmd(
            f'AWS_ACCESS_KEY_ID={config["PROD_AWS_ACCESS_KEY_ID"]} AWS_SECRET_ACCESS_KEY={config["PROD_AWS_SECRET_ACCESS_KEY"]} aws cloudfront create-invalidation --distribution-id={CLOUDFRONT_DIST_ID} --paths "/*"'
        )

        # delete build directory
        elapsed_time = time.time() - start_time
        formatted_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
        print(term.limegreen_on_black(f"==========================================="))
        print(
            term.limegreen_on_black(
                f"Frontend deploy completed in -> {formatted_time}!"
            )
        )
        print(term.limegreen_on_black(f"==========================================="))

    def rsync_frontend(self):
        print(term.limegreen_on_black("Starting frontend deploy..."))
        client = ServerService()
        start_time = time.time()
        server = client.select_server_from_list()
        FRONTEND_DIR = PROJECT_ROOT_DIR.joinpath("frontend")
        try:
            shutil.rmtree(FRONTEND_DIR.joinpath("dist").absolute())
        except FileNotFoundError:
            pass

        pkg = NPMPackage(FRONTEND_DIR.joinpath("package.json").absolute())
        pkg.run_script("build")

        ip_address = server["PublicIpAddress"]
        ssh_key = get_ssh_key()
        run_rsync(
            ssh_key_name=ssh_key,
            ip_address=ip_address,
            local_directory_path=FRONTEND_DIR.joinpath("build"),
            target_directory_path=f"/var/www/{PROJECT_NAME}/frontend",
        )

        # delete build directory
        elapsed_time = time.time() - start_time
        formatted_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
        print(term.limegreen_on_black(f"==========================================="))
        print(
            term.limegreen_on_black(
                f"Frontend deploy completed in -> {formatted_time}!"
            )
        )
        print(term.limegreen_on_black(f"==========================================="))

    def nginx(self):
        # Transfer file
        client = ServerService()
        environment = select_deploy_environment()
        server = client.select_server_from_list(environment)
        ip_address = server["PublicIpAddress"]
        ssh_key = get_ssh_key()

        if environment == EnvironmentEnum.SANDBOX:
            conf_file = 'sandbox.conf'
        else:
            conf_file = 'production.conf'

        print(term.limegreen_on_black("transferring nginx conf..."))
        start_time = time.time()
        run_scp(
            ssh_key_name=ssh_key,
            ip_address=ip_address,
            local_directory_path=PROJECT_ROOT_DIR.joinpath("infra")
            .joinpath("nginx")
            .joinpath(conf_file),
            target_directory_path=f"/etc/nginx/conf.d/{PROJECT_NAME}.conf",
        )

        print(term.limegreen_on_black("restarting nginx..."))
        run_commands_remote(
            ssh_key_name=ssh_key,
            ip_address=ip_address,
            commands=[
                "sudo service nginx restart",
            ],
        )

        elapsed_time = time.time() - start_time
        formatted_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
        print(term.limegreen_on_black(f"==========================================="))
        print(
            term.limegreen_on_black(f"nginx deploy completed in -> {formatted_time}!")
        )
        print(term.limegreen_on_black(f"==========================================="))

    def supervisor(self):
        # Transfer file
        client = ServerService()
        server = client.select_server_from_list()
        ip_address = server["PublicIpAddress"]
        ssh_key = get_ssh_key()

        print(term.limegreen_on_black("transferring supervisor conf..."))
        start_time = time.time()
        run_rsync(
            ssh_key_name=ssh_key,
            ip_address=ip_address,
            local_directory_path=INFRA_DIR / "supervisor",
            target_directory_path="/etc/",
        )

        print(term.limegreen_on_black("restarting supervisor..."))
        run_commands_remote(
            ssh_key_name=ssh_key,
            ip_address=ip_address,
            commands=[
                "sudo supervisorctl reread",
                "sudo supervisorctl update",
            ],
        )
        elapsed_time = time.time() - start_time
        formatted_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
        print(term.limegreen_on_black(f"==========================================="))
        print(
            term.limegreen_on_black(
                f"supervisorctl deploy completed in -> {formatted_time}!"
            )
        )
        print(term.limegreen_on_black(f"==========================================="))

    def datadog(self):
        # Transfer file
        client = ServerService()
        server = client.select_server_from_list()
        ip_address = server["PublicIpAddress"]
        ssh_key = get_ssh_key()

        start_time = time.time()
        print(term.limegreen_on_black("transferring datadog agent yaml..."))
        run_rsync(
            ssh_key_name=ssh_key,
            ip_address=ip_address,
            local_directory_path=INFRA_DIR / "datadog" / "conf.yaml",
            target_directory_path="/etc/datadog-agent/",
        )

        print(term.limegreen_on_black("restarting datadog agent..."))
        run_commands_remote(
            ssh_key_name=ssh_key,
            ip_address=ip_address,
            commands=[
                "sudo systemctl restart datadog-agent",
            ],
        )

        elapsed_time = time.time() - start_time
        formatted_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
        print(term.limegreen_on_black(f"==========================================="))
        print(
            term.limegreen_on_black(
                f"datadog-agent deploy completed in -> {formatted_time}!"
            )
        )
        print(term.limegreen_on_black(f"==========================================="))

    def datadog_agent(self):
        # Transfer file
        client = ServerService()
        server = client.select_server_from_list()
        ip_address = server["PublicIpAddress"]
        ssh_key = get_ssh_key()
        config = get_config()

        start_time = time.time()
        print(term.limegreen_on_black("installing datadog agent..."))
        install_command = f'DD_AGENT_MAJOR_VERSION=7 DD_API_KEY={config["DATADOG_API_KEY"]} DD_SITE="datadoghq.com" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script.sh)"'
        run_commands_remote(
            ssh_key_name=ssh_key, ip_address=ip_address, commands=[install_command]
        )

        # Enabling in datadog agent yaml
        question = [
            inquirer.Confirm(
                "edited_conf",
                message="Did you edit /etc/datadog-agent/datadog.yaml and enable APM + Logging?",
            )
        ]
        answer = inquirer.prompt(question, theme=THEME)
        if not answer["edited_conf"]:
            print(
                term.red(
                    "You may be able to set env variables instead but manual works 100%"
                )
            )

        elapsed_time = time.time() - start_time
        formatted_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
        print(term.limegreen_on_black(f"==========================================="))
        print(
            term.limegreen_on_black(
                f"datadog-agent install completed in -> {formatted_time}!"
            )
        )
        print(term.limegreen_on_black(f"==========================================="))


class Utils:
    def ssh(self):
        client = ServerService()
        environment = select_deploy_environment()
        server = client.select_server_from_list(environment=environment)
        ip_address = server["PublicIpAddress"]
        ssh_key = get_ssh_key()
        command = f"ssh -i {ssh_key} ubuntu@{ip_address}"
        print(term.limegreen_on_black(f"ssh -i {ssh_key} ubuntu@{ip_address}"))
        os.system(command)

    def status(self):
        client = ServerService()
        environment = select_deploy_environment()
        server = client.select_server_from_list(environment=environment)
        ip_address = server["PublicIpAddress"]
        ssh_key = get_ssh_key()
        run_commands_remote(
            ssh_key_name=ssh_key,
            ip_address=ip_address,
            commands=[
                "sudo supervisorctl status all",
            ],
        )
        print(term.limegreen_on_black(f"ssh -i {ssh_key} ubuntu@{ip_address}"))


class Tools:
    def __init__(self):
        self.deploy = Deploy()
        self.utils = Utils()
        self.init = Initialize()


if __name__ == "__main__":
    fire.Fire(Tools)
