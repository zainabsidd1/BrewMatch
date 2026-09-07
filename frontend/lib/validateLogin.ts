type FormErrors = {
  email?: string;
  password?: string;
};

type LoginFormData = {
  email: string;
  password: string;
};

export function validateLoginForm(data: LoginFormData): FormErrors {
  const errors: FormErrors = {};

  if (!data.email.trim()) {
    errors.email = "Email is required.";
  } else if (!data.email.includes("@")) {
    errors.email = "Enter a valid email address.";
  }

  if (!data.password) {
    errors.password = "Password is required.";
  } else if (data.password.length < 6) {
    errors.password = "Password must be at least 6 characters.";
  }

  return errors;
}
