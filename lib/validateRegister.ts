type FormErrors = {
  email?: string;
  password?: string;
  confirmPassword?: string;
};

type RegisterFormData = {
  email: string;
  password: string;
  confirmPassword: string;
};

export function validateRegisterForm(data: RegisterFormData): FormErrors {
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

  if (!data.confirmPassword) {
    errors.confirmPassword = "Please confirm your password.";
  } else if (data.confirmPassword !== data.password) {
    errors.confirmPassword = "Passwords do not match.";
  }

  return errors;
}
