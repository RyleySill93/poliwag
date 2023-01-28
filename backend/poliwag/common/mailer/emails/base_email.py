from django.core.mail import send_mail
from jinja2 import Environment, PackageLoader, select_autoescape


class BaseEmail:
    subject = None
    template_name = None
    from_email = None
    fields = tuple()
    required_context_variables = tuple()
    base_context = None

    @classmethod
    def _get_subject(cls):
        if not cls.subject:
            raise NotImplementedError("subject not specified")

        return cls.subject

    @classmethod
    def _get_template_name(cls):
        if not cls.template_name:
            raise NotImplementedError("template_name not specified")

        return cls.template_name

    @classmethod
    def _get_from_email(cls):
        if not cls.from_email:
            raise NotImplementedError("from_email not specified")

        return cls.from_email

    @classmethod
    def _get_template(cls):
        env = Environment(
            loader=PackageLoader("poliwag.common.mailer", "templates"),
            autoescape=select_autoescape(["html", "xml"]),
        )
        return env.get_template(cls.template_name)

    @classmethod
    def _get_context(cls, **kwargs):
        base_context = cls.base_context or {}
        context = {**kwargs, **base_context}

        missing_context_variables = [
            field for field in cls.required_context_variables if field not in context
        ]

        if missing_context_variables:
            raise ValueError(f"Missing context variables: {missing_context_variables}")

        return context

    @classmethod
    def send(cls, recipients, context=None):
        context = context or {}

        if not (isinstance(recipients, list) or isinstance(recipients, tuple)):
            raise ValueError("recipients must be a list or tuple")

        template = cls._get_template()

        return send_mail(
            subject=cls._get_subject(),
            message="",
            from_email=cls._get_from_email(),
            recipient_list=recipients,
            html_message=template.render(**cls._get_context(**context)),
            fail_silently=False,
        )
