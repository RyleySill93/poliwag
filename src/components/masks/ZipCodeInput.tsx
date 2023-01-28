import React from 'react';
import MaskedInput from 'react-text-mask';

const ZipCodeInput = ({ ...inputProps }: any) => {
  const shouldMaskAsZipCode = inputProps.value && inputProps.value.length > 5;

  return (
    <MaskedInput
      {...inputProps}
      mask={[/\d/, /\d/, /\d/, /\d/, /\d/, (shouldMaskAsZipCode ? '-' : /\d/), /\d/, /\d/, /\d/, /\d/]}
    />
  );
};

ZipCodeInput.defaultProps = {
  inputMode: 'numeric',
};

export default ZipCodeInput;
