<!-- Add banner here -->
![Banner](https://github.com/brandon-sharpe/MTG-project/blob/main/MTG_placeholder.gif)

# MTG Classification Project

<!-- Add buttons here -->

![GitHub release (latest by date including pre-releases)](https://img.shields.io/badge/release-draft-yellow)
![GitHub last commit](https://img.shields.io/badge/last%20commit-Oct%202021-green)

<!-- Describe your project in brief -->

# What is Magic the Gathering?
Magic: The Gathering (colloquially known as Magic or MTG) is a tabletop and digital collectible card game created by Richard Garfield. Released in 1993 by Wizards of the Coast (now a subsidiary of Hasbro), Magic was the first trading card game and had approximately thirty-five million players as of December 2018,and over twenty billion Magic cards were produced in the period from 2008 to 2016, during which time it grew in popularity. There are currently more than 20,000 unique Magic cards, to which hundreds are added each year. Cards are sold in a variety of languages and products, including booster packs and preconstructed theme decks. Magic is a game of hidden information, meaning that each player knows secrets that the other players do not. Magic cards are divided and classified by card types and color. There are 5 basic colors in MTG. White (W), Black(B), Blue(U), Green(G), and Red(R). There is also a separate colorless classification known ass Colorless(C). Cards can have multiple colors in their color identity, for example a card can be Red(R) and White(W). It is well known throughout the magic community that certain colors, or color combinations have distinct characteristics, or styles of play associated with a certain color. Blue wants to draw cards, green wants to plat large creatures as quickly as possible, black wants to bing cards back from the graveyard, red wants to play quickly and aggressively, and white likes to lose the game.  Cards are also classified by card type Sorcery, Instant, Planeswalker, Creature, Artifact, and Land.

The goal of this project is train a model to accurately predict and classify the color identity of a creature card based off of some of the attributes the card has. For the first itteration I will be focusing only on one color, but for future itterations I hope to somewhat accuratley preddict all color combinations. 

# Executive Summary
<!-- Add a demo for your project -->
- There are distinct words in the text that correlate to color

- My SVC model provides 79.74% accuracy on unseen data.

- SVC beats baseline which was was 21.48%

- These models where run soley using the text column to provide an mvp, I am confident that adding power, toughness, converted mana cost will provide a higher rate of accuracy for future iterations.

# Table of contents
<!-- Add a table of contents for your project -->

- [Project Title](#project-title)
- [What is Magic the Gathering?](#what-is-magic-the-gathering?)
- [Executive Summary](#executive-summary)
- [Table of contents](#table-of-contents)
- [Data Dictionary](#data-dictionary)
- [Data Science Pipeline](#data-science-pipline)
    - [Acquire](#acquire)
    - [Prepare](#prepare)
    - [Explore](#explore)
    - [Model](#model)
    - [Evaluate](#evaluate)
- [Conclusion](#conclusion)
- [Given More Time](#given-more-time)
- [Recreate This Project](#recreate-this-project)
- [Footer](#footer)

# Data Dictionary
[(Back to top)](#table-of-contents)
<!-- Drop that sweet sweet dictionary here-->
| Feature    | Datatype                | Definition   |
|:-----------|:------------------------|:-------------|
| colors     | 10146 non-null: object  |The color identity of the card (Target) 5 colors (Red=R,Blue=U,Green=G,White =W,Black=B)|
| keywords   | 10146 non-null: object  |Keywords used to identify common 'abilities' in the game|
| manaValue  | 10146 non-null: float64 |The resource cost used to play the card, a number|
| name       | 10146 non-null: object  |Name of the card|
| power      | 10146 non-null: object  |The attack power of the card(normally a number but can be represented by an *)|
| rarity     | 10146 non-null: object  |How rare the card was in the sets release(Common, Uncommon,Rare, Mythic Rare)|
| subtypes   | 10146 non-null: object  |Classification of a creture (ex Zombie, Dragon, Elf)|
| supertypes | 10146 non-null: object  |Classification of whether or not the creature has a supertype (Snow, Legendary, None)|
| text       | 10146 non-null: object  |Text on card, also includes keywords and explanes abilities not classified under key words|
| toughness  | 10146 non-null: object  |The defense power of a card (normally a number but can be represented by a * )             |

# Data Science Pipeline
[(Back to top)](#table-of-contents)
<!-- Describe your Data Science Pipeline process -->
Following best practices I documented my progress throughout the project and will provide quick summaries and thoughts here. For a further deep dive please visit my final notebook or take a look at the planning that took place for this project using trello (https://trello.com/b/KxhOn2jO)

### Acquire
[(Back to top)](#table-of-contents)
<!-- Describe your acquire process -->
This data was acquired from MTGJSON. MTGJSON is an open-source project that catalogs all Magic: The Gathering cards in a portable format. A dedicated group of fans maintains and supplies data for a variety of projects and sites in the community. Using an aggregation process they fetch data between multiple resources and approved partners, and combine all this data in to various JSON files that you can learn about and download from this website(https://mtgjson.com).

In particular i chose to acquire my data from the Allprintings.csv file found here(https://mtgjson.com/downloads/all-files/#allprintingscsvfiles). This file contains information on every card printed by Wizards of the Cost, including alot of information I wont be using in this project but may attempt to use in a future project.

### Prepare
[(Back to top)](#table-of-contents)
<!-- Describe your prepare process -->
- Dropped the following columns from the original dataframe ( I deemed them irrelevant to our goal)
   
       - 'index',
        - 'id',
        - 'artist',
        - 'asciiName',
        - 'borderColor',
        - 'cardKingdomEtchedId',
        - 'cardKingdomFoilId',
        - 'cardKingdomId',
        - 'colorIndicator',
        - 'duelDeck',
        - 'edhrecRank',
        - 'faceConvertedManaCost',
        - 'faceManaValue', 
        - 'faceName',
        - 'finishes',
        - 'flavorName',
        - 'flavorText',
        - 'frameEffects',
        - 'frameVersion',
        - 'hand',
        - 'hasAlternativeDeckLimit',
        - 'hasContentWarning',
        - 'hasFoil',
        - 'hasNonFoil',
        - 'isAlternative',
        - 'isFullArt',
        - 'isOversized',
        - 'isPromo',
        - 'isReserved',
        - 'isStarter',
        - 'isStorySpotlight',
        - 'isTextless',
        - 'isTimeshifted',
        - 'leadershipSkills',
        - 'life',
        - 'loyalty',
        - 'mcmId',
        - 'mcmMetaId',
        - 'mtgArenaId',
        - 'mtgjsonV4Id',
        - 'mtgoFoilId',
        - 'mtgoId',
        - 'multiverseId',
        - 'originalReleaseDate',
        - 'otherFaceIds', 
        - 'promoTypes',
        - 'purchaseUrls',
        - 'scryfallId', 
        - 'scryfallIllustrationId',
        - 'scryfallOracleId',
        - 'side',
        - 'tcgplayerEtchedProductId',
        - 'tcgplayerProductId',
        - 'uuid',
        - 'variations',
        - 'watermark',
        - 'layout',
        - 'number',
        - 'printings',
        - 'originalText',
        - 'originalType',
        - 'convertedManaCost',
        - 'manaCost'
        - 'setCode',
        - 'colorIdentity',
        - 'types',
        - 'type'
- dropped cards that are only available online then dropped correlating column
- dropped card reprints and duplicates then dropped correlating column
- converted the df to contain only creature type cards
- dropped all colorless creatures
- dropped all multicolor creatures
- dropped unhinged, unstable, unsanctioned and unglued sets from the data sets as these were joke releases with too many odditities 
- Filled null values with the word "None", in this case all nulls where acounted for and their absence was expected
-  we had to search the text for the tap symbol to effectivley use nlp
- we had to remove the mana symbols from the text of the card because it is leaked data 
- removing name of each card from the cards text to avoid overfitting on classification models later replaced it with "This"
- removed all symnols and text that might confuse nlp ('\([^)]*\)

### Explore
[(Back to top)](#table-of-contents)
<!-- Describe your explore process -->
Tested multiple hypothesis including:
    - Diffence in mean mans values between colors
    - Difference in mean power between colors
    - difference in mean toughness between colors
Viewed the top 25 words for each color, found a significant difference
    
### Model
[(Back to top)](#table-of-contents)
<!-- Describe your modeling process -->
Baseline was set using the most frequent color which was green and 21.48%

Ran over 100 different models including:
 - Support Vector Classifier
 - Logistic Regression
 - K Nearest Neighbor
 - Decision Trees
 - Random Forrest

### Evaluate
[(Back to top)](#table-of-contents)
<!-- Describe your evaluation process -->
Best performing model was a Support Vector Classifier which had 79.74% accuracy on unseen data


# Conclusion
[(Back to top)](#table-of-contents)
<!-- Wrap up with conclusions and takeaways -->
- SVM was our best performing model beating our baseline by 58.26% on unseen data
- These models were run using ONLY the text on the card to get to an mvp, Im confident future iterations will bring more accuracy with the inclusion of power, toughness, and converted mana cost, and creature type

# Given More Time
[(Back to top)](#table-of-contents)
<!-- LET THEM KNOW WHAT YOU WISH YOU COULD HAVE DONE-->
- As I mentioned in the conclusion future iterations will include creature type, power, toughness, and converted mana cost. 
- I would like to try stemming my word bag to see if it effects accuracy, these

# Recreate This Project
[(Back to top)](#table-of-contents)
<!-- How can they do what you do?-->
Run these commands in a python enviorment:

import nltk

nltk.download('punkt')

Download into the same folder:
https://mtgjson.com/downloads/all-files/#allprintingscsvfiles

my wrangle.py

my notebook

# Footer
[(Back to top)](#table-of-contents)
<!-- LET THEM KNOW WHO YOU ARE (linkedin links) close with a joke. -->

If you have anyquestions please feel free to reach out to me.
