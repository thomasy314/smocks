import { FormEvent } from "react";
import UsernamePasswordForm from "../commonComponents/usernamePasswordForm";

type BasicAuthRegister = {
  registerFunc: (username: string, password: string) => Promise<boolean>;
  onRegisterFailure?: (username: string, password: string) => Promise<boolean>;
  onRegisterSuccessful?: (
    username: string,
    password: string
  ) => Promise<boolean>;

  checkLoginFunc: (username: string, password: string) => Promise<boolean>;
  onLoginSuccessful?: (username: string, password: string) => void;
  onLoginFailure?: (username: string, password: string) => void;
};

function BasicAuthRegister({
  registerFunc,
  onRegisterFailure,
  onRegisterSuccessful,
}: BasicAuthRegister) {
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

    const registerSuccessful = await registerFunc(username, password);

    if (registerSuccessful && onRegisterSuccessful) {
      onRegisterSuccessful(username, password);
    } else if (onRegisterFailure) {
      onRegisterFailure(username, password);
    }
  }

  return <UsernamePasswordForm onSubmit={handleSubmit} />;
}

export default BasicAuthRegister;
