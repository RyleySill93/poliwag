export type OnboardingStatusType = 'ACCOUNT_DETAILS' | 'ABOUT_YOU' | 'SUITABILITY' | 'COMPLIANCE' | 'OPEN_YOUR_ACCOUNT' | 'TRANSFER_SHARES'
export type EntityMembershipRoleType = 'ADMIN';
export type EntityTypeType = 'USER' | 'TRUST' | 'INVESTOR'

export type EntityType = {
    id: string;
    name: string;
    type: EntityTypeType;
}

export type EntityMembershipWithEntityType = {
    id: string;
    userId: string;
    entity: EntityType;
    role: EntityMembershipRoleType;
}

export type UserType = {
    firstName: string;
    lastName: string;
    fullLegalName: string;
    onboardingStatus: OnboardingStatusType;
    entityMemberships: EntityMembershipWithEntityType[];
};
