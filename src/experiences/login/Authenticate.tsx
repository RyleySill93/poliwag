import React from 'react';

import EnterYourPhoneNumber from './EnterYourPhoneNumber';
import SixDigitCode from './SixDigitCode';

type Props = {
  title: string;
  subtitle: string;
  confirmCode: (code: string) => void;
  onPhoneEntered: (phone: string) => void;
  phone: string;
  showLoginLink?: boolean;
}

const Authenticate = ({
  title,
  subtitle,
  confirmCode,
  onPhoneEntered,
  phone,
  showLoginLink
}: Props) => {
  if (phone) return <SixDigitCode phone={phone} confirmCode={confirmCode} />;

  return (
    <EnterYourPhoneNumber
      title={title}
      subtitle={subtitle}
      onPhoneEntered={onPhoneEntered}
      showLoginLink={showLoginLink}
    />
  );
};

export default Authenticate;
