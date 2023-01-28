import React from 'react';

const useModal = (initialIsOpen = false) => {
  const [isOpen, setIsOpen] = React.useState(initialIsOpen);
  const [modalContent, setModalContent] = React.useState<any>();

  const openModal = (content?: any) => {
    setModalContent(content);
    setIsOpen(true);
  };

  const closeModal = () => {
    setIsOpen(false);
    setModalContent(undefined);
  };

  return {
    isOpen, openModal, closeModal, modalContent
  };
};

export default useModal;
