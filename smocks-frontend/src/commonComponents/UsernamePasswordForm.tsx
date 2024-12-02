import { FormEvent } from "react";
import "./UsernamePasswordForm.css";

type UsernamePasswordFormProps = {
  onSubmit: (event: FormEvent<HTMLFormElement>) => void;
};

function UsernamePasswordForm({ onSubmit }: UsernamePasswordFormProps) {
  return (
    <form className="usernamePasswordForm" onSubmit={onSubmit}>
      <input type="text" placeholder="username" name="username" />
      <input type="password" placeholder="password" name="password" />
      <input type="submit" value="submit" />
    </form>
  );
}

export default UsernamePasswordForm;
