import logging

from card_live_dashboard.model.data_modifiers.CardLiveDataModifier import CardLiveDataModifier
from card_live_dashboard.model.CardLiveData import CardLiveData
from card_live_dashboard.model.RGIParser import RGIParser
from card_live_dashboard.service.TaxonomicParser import TaxonomicParser

logger = logging.getLogger(__name__)


class AddTaxonomyModifier(CardLiveDataModifier):

    def __init__(self):
        """
        Builds a new modifier which will add in taxonomy categories.
        """
        super().__init__()

    def modify(self, data: CardLiveData) -> CardLiveData:
        logger.debug(f'Main df before {data.main_df}')
        taxonomy_parser = TaxonomicParser(df_rgi_kmer=data.rgi_kmer_df, df_lmat=data.lmat_df)
        matches_df = taxonomy_parser.create_file_matches().rename(
            columns={'lmat.taxonomy_label': 'lmat_taxonomy',
                     'rgi_kmer.taxonomy_label': 'rgi_kmer_taxonomy'
                     }
        )
        matches_df = matches_df.drop(columns=['matches'])
        main_df = data.main_df.merge(matches_df, left_index=True, right_index=True, how='left')
        logger.debug(f'Main df after {main_df}')

        rgi_df = data.rgi_df.copy()
        rgi_kmer_df = data.rgi_kmer_df.copy()
        lmat_df = data.lmat_df.copy()
        mlst_df = data.mlst_df.copy()

        return CardLiveData(main_df=main_df,
                            rgi_parser=RGIParser(rgi_df),
                            rgi_kmer_df=rgi_kmer_df,
                            mlst_df=mlst_df,
                            lmat_df=lmat_df)