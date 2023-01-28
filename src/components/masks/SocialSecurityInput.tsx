import React from 'react';
import MaskedInput from 'react-text-mask';

const SocialSecurityMask = ({ ...inputProps }: any) => (
  <MaskedInput
    {...inputProps}
    mask={[/\d/, /\d/, /\d/, '-', /\d/, /\d/, '-', /\d/, /\d/, /\d/, /\d/]}
  />
);

SocialSecurityMask.defaultProps = {
  inputMode: 'numeric',
};

export default SocialSecurityMask;
