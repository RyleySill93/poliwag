import jwtDecode from 'jwt-decode';

const SESSION = 'SESSION';

class AuthService {
  handleAuthentication = (session: any) => {
    if (!session) return;

    if (this.isValidToken(session.access)) {
      this.setSession(session);
    } else {
      this.logout();
    }
  }

  logout = () => this.setSession(null);

  setSession = (session: string | null) => {
    if (session) {
      localStorage.setItem(SESSION, JSON.stringify(session));
    } else {
      localStorage.removeItem(SESSION);
    }
  }

  getSession = () => {
    const session = localStorage.getItem(SESSION);

    if (session) return JSON.parse(session);

    return null;
  };

  isValidToken = (access: any) => {
    if (!access) {
      return false;
    }

    const decoded = jwtDecode(access);
    const currentTime = Date.now() / 1000;

    // @ts-ignore
    return decoded.exp > currentTime;
  }

  isAuthenticated = () => !!this.getSession()
}

const authService = new AuthService();

export default authService;
