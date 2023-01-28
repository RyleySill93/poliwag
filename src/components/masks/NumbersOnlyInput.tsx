import React from 'react';
import MaskedInput from 'react-text-mask';
import { createNumberMask } from 'text-mask-addons';

const defaultMaskOptions = {
  prefix: '',
  suffix: '',
  includeThousandsSeparator: true,
  allowDecimal: false,
  integerLimit: null,
  allowNegative: false,
};

const NumbersOnlyInput = ({ maskOptions, ...inputProps }: any) => {
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

NumbersOnlyInput.defaultProps = {
  inputMode: 'numeric',
  maskOptions: {},
};

export default NumbersOnlyInput;
