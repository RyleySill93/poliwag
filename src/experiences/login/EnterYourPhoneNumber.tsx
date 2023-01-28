import React from 'react';
import { useFormik } from 'formik';
import * as yup from 'yup';
import { useNavigate } from 'react-router';
import {
  Box, Button, Link, Typography
} from '@mui/material';

import FormikTextField from '../../components/formik/FormikTextField';
import Layout from '../components/Layout';

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

const EnterYourPhoneNumber = ({
  title,
  subtitle,
  onPhoneEntered,
  showLoginLink
}: Props) => {
  const navigate = useNavigate();
  const formik = useFormik({
    initialValues: {
      phone: '',
    },
    validationSchema,
    onSubmit: (values: { phone: string }) => onPhoneEntered(values.phone),
  });

  return (
    <Layout
      withLogin
      footer={(
        <Button variant="contained" size="large" fullWidth onClick={formik.submitForm}>
          Continue
        </Button>
      )}
    >
      <Typography variant="h2" mb={1}>
        {title}
      </Typography>
      <Typography variant="body2" color="textSecondary">
        {subtitle}
      </Typography>
      <form onSubmit={formik.handleSubmit}>
        <Box mt={3}>
          <FormikTextField
            name="phone"
            formik={formik}
            label="Mobile number"
            autoComplete="tel-national"
            inputProps={{
              autoComplete: 'tel-national'
            }}
            fullWidth
            mask="phone"
            sx={{ mb: 1 }}
          />
          {
            showLoginLink ? (
              <Link variant="body2" onClick={() => navigate('/login')}>
                Already have an account? Login
              </Link>
            ) : null
          }
        </Box>
      </form>

    </Layout>
  );
};

export default EnterYourPhoneNumber;
