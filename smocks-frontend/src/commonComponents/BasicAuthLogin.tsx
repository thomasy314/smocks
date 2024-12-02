import { FormEvent } from "react";

type LoginProps = {
  checkLoginFunc: (username: string, password: string) => Promise<boolean>;
  onLoginSuccessful?: (username: string, password: string) => void;
  onLoginFailure?: (username: string, password: string) => void;
};

function BasicAuthLogin({
  checkLoginFunc,
  onLoginFailure,
  onLoginSuccessful,
}: LoginProps) {
  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const formData = new FormData(event.target as HTMLFormElement);

    const username = formData.get("username")?.toString();
    const password = formData.get("password")?.toString();

    (event.target as HTMLFormElement).reset();

    if (!username || !password) {
      return;
    }

    const loginSuccessful = await checkLoginFunc(username, password);

    if (loginSuccessful && onLoginSuccessful) {
      onLoginSuccessful(username, password);
    } else if (onLoginFailure) {
      onLoginFailure(username, password);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input type="text" placeholder="username" name="username" />
      <input type="password" placeholder="password" name="password" />
      <input type="submit" />
    </form>
  );
}

export default BasicAuthLogin;
