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
  decimalLimit: 2, // how many digits allowed after the decimal
  integerLimit: null, // limit length of integer numbers
  allowNegative: false,
  allowLeadingZeroes: false,
};

const CurrencyInput = ({ maskOptions, ...inputProps }: any) => {
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

CurrencyInput.defaultProps = {
  inputMode: 'numeric',
  maskOptions: {},
};

export default CurrencyInput;
