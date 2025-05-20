from .base import *

class Company(GraphQL):
    tax_exemptions = ["CA_BC_COMMERCIAL_FISHERY_EXEMPTION","CA_BC_CONTRACTOR_EXEMPTION","CA_BC_PRODUCTION_AND_MACHINERY_EXEMPTION","CA_BC_RESELLER_EXEMPTION","CA_BC_SUB_CONTRACTOR_EXEMPTION","CA_DIPLOMAT_EXEMPTION","CA_MB_COMMERCIAL_FISHERY_EXEMPTION","CA_MB_FARMER_EXEMPTION","CA_MB_RESELLER_EXEMPTION","CA_NS_COMMERCIAL_FISHERY_EXEMPTION","CA_NS_FARMER_EXEMPTION","CA_ON_PURCHASE_EXEMPTION","CA_PE_COMMERCIAL_FISHERY_EXEMPTION","CA_SK_COMMERCIAL_FISHERY_EXEMPTION","CA_SK_CONTRACTOR_EXEMPTION","CA_SK_FARMER_EXEMPTION","CA_SK_PRODUCTION_AND_MACHINERY_EXEMPTION","CA_SK_RESELLER_EXEMPTION","CA_SK_SUB_CONTRACTOR_EXEMPTION","CA_STATUS_CARD_EXEMPTION","EU_REVERSE_CHARGE_EXEMPTION_RULE","US_AK_RESELLER_EXEMPTION","US_AL_RESELLER_EXEMPTION","US_AR_RESELLER_EXEMPTION","US_AZ_RESELLER_EXEMPTION","US_CA_RESELLER_EXEMPTION","US_CO_RESELLER_EXEMPTION","US_CT_RESELLER_EXEMPTION","US_DC_RESELLER_EXEMPTION","US_DE_RESELLER_EXEMPTION","US_FL_RESELLER_EXEMPTION","US_GA_RESELLER_EXEMPTION","US_HI_RESELLER_EXEMPTION","US_IA_RESELLER_EXEMPTION","US_ID_RESELLER_EXEMPTION","US_IL_RESELLER_EXEMPTION","US_IN_RESELLER_EXEMPTION","US_KS_RESELLER_EXEMPTION","US_KY_RESELLER_EXEMPTION","US_LA_RESELLER_EXEMPTION","US_MA_RESELLER_EXEMPTION","US_MD_RESELLER_EXEMPTION","US_ME_RESELLER_EXEMPTION","US_MI_RESELLER_EXEMPTION","US_MN_RESELLER_EXEMPTION","US_MO_RESELLER_EXEMPTION","US_MS_RESELLER_EXEMPTION","US_MT_RESELLER_EXEMPTION","US_NC_RESELLER_EXEMPTION","US_ND_RESELLER_EXEMPTION","US_NE_RESELLER_EXEMPTION","US_NH_RESELLER_EXEMPTION","US_NJ_RESELLER_EXEMPTION","US_NM_RESELLER_EXEMPTION","US_NV_RESELLER_EXEMPTION","US_NY_RESELLER_EXEMPTION","US_OH_RESELLER_EXEMPTION","US_OK_RESELLER_EXEMPTION","US_OR_RESELLER_EXEMPTION","US_PA_RESELLER_EXEMPTION","US_RI_RESELLER_EXEMPTION","US_SC_RESELLER_EXEMPTION","US_SD_RESELLER_EXEMPTION","US_TN_RESELLER_EXEMPTION","US_TX_RESELLER_EXEMPTION","US_UT_RESELLER_EXEMPTION","US_VA_RESELLER_EXEMPTION","US_VT_RESELLER_EXEMPTION","US_WA_RESELLER_EXEMPTION","US_WI_RESELLER_EXEMPTION","US_WV_RESELLER_EXEMPTION","US_WY_RESELLER_EXEMPTION"]
    def setLocationTaxExemptions(self,location):
        if location["shippingAddress"] is not None:
            if len(location["taxExemptions"])<1:
                location_exemptions = list(filter(lambda c: f"_{location['shippingAddress']['zoneCode']}_" in c,self.tax_exemptions))
                if len(location_exemptions)>0:
                    logger.error(f"Updating Tax exemptions for {location['id']}")
                    ret = self.run(
                    """
                        mutation companyLocationAssignTaxExemptions($companyLocationId: ID!, $taxExemptions: [TaxExemption!]!) {
                            companyLocationAssignTaxExemptions(companyLocationId: $companyLocationId, taxExemptions: $taxExemptions) {
                                companyLocation {
                                    # CompanyLocation fields
                                    id
                                    shippingAddress {
                                        zoneCode
                                    }
                                    taxExemptions
                                }
                                userErrors {
                                    field
                                    message
                                }
                            }
                        }
                        """,
                        {
                            "companyLocationId": location["id"],
                            "taxExemptions":location_exemptions
                        }
                    )
 