import React from 'react';
import { FormikContextType } from 'formik';
import DrawerSelect, { Props as DrawerSelectProps } from '../DrawerSelect';

type Props = Omit<DrawerSelectProps, 'onChange' | 'value'> & {
  formik: FormikContextType<any>;
  name: string;
}

const FormikDrawerSelect = ({
  formik,
  name,
  ...props
}: Props) => (
  <DrawerSelect
    {...props}
    name={name}
    value={formik.values[name]}
    onChange={(value: string) => formik.setFieldValue(name, value)}
    // @ts-ignore
    error={formik.touched[name] && Boolean(formik.errors[name])}
    // @ts-ignore
    helperText={formik.touched[name] && formik.errors[name]}
  />
);

export default FormikDrawerSelect;
