export type StepType = 'YOUR_DETAILS' | 'YOUR_SHARES' | 'GET_STARTED'

export type TransactionStatusType = 'PENDING' | 'EXECUTED' | 'SETTLED' | 'CANCELED';
export type TransactionTypeType = 'TRANSFER' | 'SALE';

export type TransactionType = {
    type: TransactionTypeType;
    status: TransactionStatusType;
    saleAmount: string;
    initiatedAt: string;
    fromEntityName: string;
    toEntityName: string;
    shareQty: string;
};

export type PortfolioType = {
    totalValue: string;
};

export type IssuerType = {
    id: string;
    name: string;
}
