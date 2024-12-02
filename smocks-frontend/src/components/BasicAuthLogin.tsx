import { FormEvent } from "react";
import UsernamePasswordForm from "../commonComponents/usernamePasswordForm";

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

    const formElement = event.target as HTMLFormElement;

    const formData = new FormData(formElement);

    const username = formData.get("username")?.toString();
    const password = formData.get("password")?.toString();

    formElement.reset();

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

  return <UsernamePasswordForm onSubmit={handleSubmit} />;
}

export default BasicAuthLogin;
