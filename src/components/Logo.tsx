import React from 'react';

type Props = {
  width?: number;
};

export default function Logo({ width }: Props) {
  return (
    <img src="/logo.png" alt="Poliwag logo" width={width} />
  );
}
