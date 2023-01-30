import React from 'react';
import { useFormik } from 'formik';
import * as yup from 'yup';
import { useNavigate } from 'react-router';
import {
  Box, Button, Card, Link, Typography
} from '@mui/material';

import FormikTextField from '../../components/formik/FormikTextField';
import Logo from '../../components/Logo';

const validationSchema = yup.object({
  phone: yup
    .string() // @ts-ignore
    .test('phone', 'Invalid phone number', (val: string) => val?.match(/\d/g).length === 10)
    .required('Phone number is required'),
});

type Props = {
  title: string;
  subtitle: string;
  onPhoneEntered: (phone: string) => void;
  showLoginLink?: boolean;
};

const Login = ({ }: Props) => {
  const navigate = useNavigate();
  const formik = useFormik({
    initialValues: {
      phone: '',
    },
    validationSchema,
    onSubmit: (values: { phone: string }) => onPhoneEntered(values.phone),
  });

  return (
    <Box display="flex" alignItems="center" justifyContent="center" height="100%" flexDirection="column">
      <Logo width={126} />
      <Card
        sx={{
          px: 5,
          py: 6,
          width: 375
        }}
      >
        <Typography variant="h4" mb={1} textAlign="center">
          Log in to your account
        </Typography>
        <form onSubmit={formik.handleSubmit}>
          <Box mt={3}>
            <FormikTextField
              name="email"
              label="Email address"
              formik={formik}
              fullWidth
              sx={{ mb: 2 }}
            />
            <FormikTextField
              name="password"
              label="Password"
              formik={formik}
              fullWidth
              sx={{ mb: 4 }}
            />
            <Button variant="contained" fullWidth>
              Continue
            </Button>
            <Typography variant="body2" mt={3} textAlign="center">
              Don't have an account?&nbsp;
              <Link variant="body2" onClick={() => navigate('/sign-up')} textAlign="center" sx={{ cursor: 'pointer' }}>
                Sign Up
              </Link>
            </Typography>
          </Box>
        </form>
      </Card>
      <Typography variant="body2" mt={3} textAlign="center">
        Having trouble logging in?&nbsp;
        <Link variant="body2" onClick={() => navigate('/forgot-password')} textAlign="center" sx={{ cursor: 'pointer' }}>
          Click here
        </Link>
        &nbsp;to set a new password.
      </Typography>
    </Box>
  );
};

export default Login;
