import pandas as pd
import numpy as np
import re
import nltk
from sklearn.model_selection import train_test_split


def vampyric_tutor():
    '''This function will read in the locally stored csv file containing every MTG card'''
    df = pd.read_csv('cards.csv')
    return df

def tap(x):
    '''This function searches for the Tap symbol and replaces it with the word Tap '''
    return re.sub("{T}" , "Tap ", x)

def remove_mana(x):
    '''This function searches for mana symbols within the card and replaces it with a 1'''
    return re.sub("{[A-Z]}" , "{1}", x)

def remove_name(df):
    '''This function removes the cards name from the text to avoid overfitting and replaces it with this   card'''
    for i in range(len(df)):
        df['text'][i] = re.sub(df['name'][i] , "this card", df['text'][i])
    return df

def remove_code_text(x):
    '''This function will remove all of the left over code from when it was in json format'''
    return re.sub('\([^)]*\)' , "", x)

def stem_words(x):
    '''This function will stemm the words of a dataframe'''
    stems = [ps.stem(word) for word in (x).split()]
    df_stemmed = ' '.join(stems)
    return df_stemmed

def bannana_split(df):
    '''This function will split our data into a train, validate and test df stratifying color'''
    train_validate, test = train_test_split(df, test_size=.2, 
                                        random_state=411, 
                                        stratify=df.colors)
    train, validate = train_test_split(train_validate, test_size=.3, 
                                   random_state=411, 
                                   stratify=train_validate.colors)
    return train, validate, test

def cyclonic_rift(df):    
    '''This function takes in a dataframe of MTG cards, drops columns deemed irrelevant to the
    goal(check README.MD for more info). Drops all online only cards, Reprints of cards, limits the card pool to single color creature cards'''
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
    # Fills null values with the word "None"
    df.keywords.fillna(value= "None", inplace=True)
    df.supertypes.fillna(value= "None", inplace=True)
    df.text.fillna(value= "None", inplace=True)
    df.subtypes.fillna(value= "Namless", inplace=True)
    df.reset_index(drop= True, inplace= True)
    
    
    # we had to search the text for the tap symbol to effectivley use nlp and so it didnt hurt the 
    #remove mana funtion
    df.text = df.text.apply(tap)
    # we had to remove the mana symbols from the text of the card because it is leaked data 
    df.text = df.text.apply(remove_mana)
    # removing name from text to avoid overfitting on classification models later 
    df = remove_name(df)
    # remove the new line text(\n and \) from json format
    df['text'].replace("\n" , " ", inplace=True, regex=True)
    df['text'].replace("\'" , "", inplace=True, regex=True)
    df.text = df.text.apply(remove_code_text)
    df = df[df.colors != "C"]
    df = df[((df.toughness != '*') & (df.toughness != '1+*') & 
               (df.toughness != '*+1') & 
               (df.toughness != '2+*') & (df.toughness != '?')
            )]
    df.toughness = df.toughness.astype(float)
    df = df[((df.power != '*') & (df.power != '1+*') & 
               (df.power != '*+1') & 
               (df.power != '2+*') & (df.power != '?'))]
    df.power = df.power.astype(float)
    df.manaValue = df.manaValue.astype(float)
    df.dropna(inplace=True)
    return df


def wrangle():
    '''Returns cleaned and prepped dataframe'''
    df = vampyric_tutor()
    df =  cyclonic_rift(df)
    train,validate,test = bannana_split(df)
    return train,validate,test
