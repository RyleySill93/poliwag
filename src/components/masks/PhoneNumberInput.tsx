import React from 'react';
import MaskedInput from 'react-text-mask';

const PhoneNumberInput = ({ ...inputProps }: any) => (
  <MaskedInput
    {...inputProps}
    mask={['(', /[1-9]/, /\d/, /\d/, ')', ' ', /\d/, /\d/, /\d/, '-', /\d/, /\d/, /\d/, /\d/]}
  />
);

PhoneNumberInput.defaultProps = {
  inputMode: 'numeric',
};

export default PhoneNumberInput;
