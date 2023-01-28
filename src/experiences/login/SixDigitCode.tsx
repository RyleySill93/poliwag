import React from 'react';
import * as yup from 'yup';
import {
  Box, Button, Link, Typography
} from '@mui/material';
import { useFormik } from 'formik';
import { useSnackbar } from 'notistack';
// eslint-disable-next-line import/no-extraneous-dependencies
import throttle from 'lodash.throttle';

import Layout from '../components/Layout';
import TapClient from '../../utils/tapClient';
import FormikOtpInput from '../../components/formik/FormikOtpInput';

const validationSchema = yup.object({
  code: yup
    .string()
    .min(2, 'Code is required')
    .required('Code is required'),
});

type Props = {
  phone: string;
  confirmCode: (code: string) => void;
}

const SixDigitCode = ({ phone, confirmCode }: Props) => {
  const { enqueueSnackbar } = useSnackbar();
  const formik = useFormik({
    initialValues: {
      code: '',
    },
    validationSchema,
    onSubmit: (values) => confirmCode(values.code),
  });

  const resendCode = () => new TapClient('/auth/phone/generate/', { phone }).post().then(() => {
    enqueueSnackbar('Code sent.', {
      variant: 'success'
    });
  });
  const onResendCode = throttle(() => resendCode(), 3000);

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
        6-digit code
      </Typography>
      <Box>
        <Typography variant="body2" color="textSecondary">
          We sent a 6-digit verification code to
        </Typography>
        <Typography variant="body2">
          {` ${phone}.`}
        </Typography>
      </Box>
      <form onSubmit={formik.handleSubmit}>
        <Box mt={3}>
          <FormikOtpInput
            name="code"
            id="one-time-code"
            formik={formik}
          />
          <Link variant="body2" onClick={() => onResendCode()}>
            Resend code
          </Link>
        </Box>
      </form>
    </Layout>
  );
};

export default SixDigitCode;
