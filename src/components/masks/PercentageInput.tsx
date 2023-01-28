import React from 'react';
import MaskedInput from 'react-text-mask';
import { createNumberMask } from 'text-mask-addons';

const defaultMaskOptions = {
  prefix: '',
  suffix: '',
  includeThousandsSeparator: true,
  thousandsSeparatorSymbol: ',',
  allowDecimal: true,
  decimalSymbol: '.',
  decimalLimit: null, // how many digits allowed after the decimal
  integerLimit: 2, // limit length of integer numbers
  allowNegative: false,
  allowLeadingZeroes: true,
};

const PercentageInput = ({ maskOptions, ...inputProps }: any) => {
  const currencyMask = createNumberMask({
    ...defaultMaskOptions,
    ...maskOptions,
  });

  const unmask = (maskedValue: any) => maskedValue.replace(/[, ]+/g, '');

  return (
    <MaskedInput
      {...inputProps}
      onChange={(e: any) => {
        e.target.rawValue = unmask(e.target.value);
        inputProps.onChange(e);
      }}
      mask={currencyMask}
    />
  );
};

PercentageInput.defaultProps = {
  inputMode: 'numeric',
  maskOptions: {},
};

export default PercentageInput;
