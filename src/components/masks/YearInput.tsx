import React from 'react';
import MaskedInput from 'react-text-mask';
import { createNumberMask } from 'text-mask-addons';

const defaultMaskOptions = {
  prefix: '',
  suffix: '',
  includeThousandsSeparator: false,
  allowDecimal: false,
  integerLimit: 4,
  allowNegative: false,
  allowLeadingZeroes: false,
};

const YearInput = ({ maskOptions, ...inputProps }: any) => {
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

YearInput.defaultProps = {
  inputMode: 'numeric',
  maskOptions: {},
};

export default YearInput;
