import pandas as pd
import numpy as np

def vampyric_tutor():
    '''This function will read in the locally stored csv file containing every MTG card'''
    df = pd.read_csv('cards.csv')
    return df
def cyclonic_rift(df):    
    '''This function takes in a dataframe of MTG cards, drops columns deemed irrelevant to the
    goal(check README.MD for more info). Drops all online only cards, Reprints of cards, limits the card pool 
    to single color creature cards'''
    # drop columns that are irrelevant to our goal.
    df = df.drop(columns=
            ['index',
             'id',
             'artist',
             'asciiName',
             'borderColor',
             'cardKingdomEtchedId',
             'cardKingdomFoilId',
             'cardKingdomId',
             'colorIndicator',
             'duelDeck',
             'edhrecRank',
             'faceConvertedManaCost',
             'faceManaValue', 
             'faceName',
             'finishes',
             'flavorName',
             'flavorText',
             'frameEffects',
             'frameVersion',
             'hand',
             'hasAlternativeDeckLimit',
             'hasContentWarning',
             'hasFoil',
             'hasNonFoil',
             'isAlternative',
             'isFullArt',
             'isOversized',
             'isPromo',
             'isReserved',
             'isStarter',
             'isStorySpotlight',
             'isTextless',
             'isTimeshifted',
             'leadershipSkills',
             'life',
             'loyalty',
             'mcmId',
             'mcmMetaId',
             'mtgArenaId',
             'mtgjsonV4Id',
             'mtgoFoilId',
             'mtgoId',
             'multiverseId',
             'originalReleaseDate',
             'otherFaceIds', 
             'promoTypes',
             'purchaseUrls',
             'scryfallId', 
             'scryfallIllustrationId',
             'scryfallOracleId',
             'side',
             'tcgplayerEtchedProductId',
             'tcgplayerProductId',
             'uuid',
             'variations',
             'watermark',
             'layout',
             'number',
             'printings',
             'originalText',
             'originalType',
             'convertedManaCost',
             'manaCost'])

    # drop cards that are only available online then drop the column
    df = df[df.isOnlineOnly==0]
    df = df.drop(columns=
            ['availability',
             'isOnlineOnly'])

    # drop all duplications and reprints of cards then drop the column
    df = df[df.isReprint==0]
    df = df.drop(columns=
            ['isReprint'])

    # makes the df contain only creature type cards
    df = df[df.types.str.contains('Creature', regex=False)]

    # makes a new color for colorless createarues
    df.colorIdentity.fillna(value= "C", inplace=True)
    df.colors.fillna(value= "C", inplace=True)

    #for the first iteration i will only be focusing on creatres with a single color identity 
    df = df[df.colorIdentity.str.len() == 1]
    # drop unhinged, unstable, unsanctioned and unglued sets from the data sets as these were joke releases 
    df = df[(df.setCode != 'UST')&(df.setCode !='UNH')&(df.setCode !='UND')&(df.setCode !='UGL')]
    df = df.drop(columns=
            ['setCode',
            'colorIdentity',
            'types',
            'type'])
    return df
def wrangle():
    '''Returns cleaned and prepped dataframe'''
    df = vampyric_tutor()
    df =  cyclonic_rift(df)
    return df