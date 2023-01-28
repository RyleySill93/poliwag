import React from 'react';
import {
  InputAdornment,
} from '@mui/material';
import { InputProps as StandardInputProps } from '@mui/material/Input/Input';

import MuiTextField, { TextFieldProps as MuiTextFieldProps } from '@mui/material/TextField';
import CurrencyInput from './masks/CurrencyInput';
import PercentageInput from './masks/PercentageInput';
import PhoneNumberInput from './masks/PhoneNumberInput';
import SocialSecurityMask from './masks/SocialSecurityInput';
import NumbersOnlyInput from './masks/NumbersOnlyInput';
import YearInput from './masks/YearInput';
import ZipCodeInput from './masks/ZipCodeInput';

export type TextFieldProps = MuiTextFieldProps & {
  mask?: 'currency' | 'phone' | 'ssn' | 'percentage' | 'year' | 'zipCode' | 'number';
  InputProps?: StandardInputProps;
}

const TextField = ({
  mask,
  ...props
}: TextFieldProps) => {
  const inputProps: StandardInputProps = {
    ...props.InputProps,
  };

  if (mask === 'currency') {
    // @ts-ignore
    inputProps.inputComponent = CurrencyInput;
    inputProps.startAdornment = <InputAdornment position="start">$</InputAdornment>;
  } else if (mask === 'phone') {
    // @ts-ignore
    inputProps.inputComponent = PhoneNumberInput;
  } else if (mask === 'ssn') {
    // @ts-ignore
    inputProps.inputComponent = SocialSecurityMask;
  } else if (mask === 'percentage') {
    inputProps.endAdornment = <InputAdornment position="start">%</InputAdornment>;
    // @ts-ignore
    inputProps.inputComponent = PercentageInput;
  } else if (mask === 'year') {
    // @ts-ignore
    inputProps.inputComponent = YearInput;
    // @ts-ignore
  } else if (mask === 'zipCode') {
    // @ts-ignore
    inputProps.inputComponent = ZipCodeInput;
  } else if (mask === 'number') {
    // @ts-ignore
    inputProps.inputComponent = NumbersOnlyInput;
  }

  return (
    <MuiTextField
      variant="outlined"
      fullWidth
      {...props}
      required={false}
      InputProps={inputProps}
    />
  );
};

export default TextField;
