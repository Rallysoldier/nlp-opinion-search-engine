# nlp-opinion-search-engine

TODO:
    QC:
    1. Ensure correct ID's in the... 
       posting_list.pkl, CHECK
       review_metadata.pkl, 
       result.pkl, 
       final output pkl. (method)
            -Cross check against reviews_segment.xlsx to ensure purity
    
    Analytics:
    1. Turn method final output pkls into xlsx
    2. Analyze contents for accuracy
    3. Precision/retention/etc
    4. Reference file for findings that is built on, not replaced
        (ENSURE YOU BACKUP IN CASE PROGRAM FUCKS UP)
    i.e., xlsx_analyzer.py

    Maybe:
    1. Use analytic findings to improve classifier
    1.5. Search for bigrams in text confirmed as correctly positive, negative, retrain classifier 
    2(UNIQUE). Search for repeat reviewers by customer ID, create profile for each customer, giving a weight 
    based on the average positivity ratio of all their comments. 
        --NEED: Create class Customer: 
            float positivity_ratio
            int num_comments
            int helpful_count (increases the weight of their positivity in overall calculations)
            def weight()
    3. Modify pos/neg lexicon, create more complex lexicon with tags for each word:
        OR implement into ratio calculator, giving preference to or even overriding results in combined_result for perfect scores.
        1. tag = 1 (Perfectly Negative)
        2. tag = 2 (Predominately Negative)
        3. tag = 3 (Mixed)
        4. tag = 4 (Predominately Positive)
        5. tag = 5 (Perfectly Positive)
    3.5 ALTERNATE: For each word in the pos/neg lexicon, append a sum: For every review it appears in, sum the stars together.
        The average star rating is then applied to the word as a tag (seen above).
        Then, Based on the tag of the opinion word, narrow the search to retrieve truly negative, truly mixed, or truly positive reviews.

    (10)
    'Look at the review by C-Net and you start to realize that here is another Cisco/Linksys product that just DOES NOT WORK.\nI am not a computer expert and don\'t have the time to become one.\nWhen I spend the better part of $100.00 I expect the product to work.\nThe Wireless-G Music Bridge doesn\'t work.\nIt especially doesn\'t work with Windows Vista Ultimate.\nDon\'t buy this product and write to Cisco/Linksys to let them know how dissatisfied you are with their products that make you be a computer expert to make them work.\nWhat ever happened with the promise of "Plug and Play."'
    
    (8)
    'Book is good, interesting, but pretty short.  (And very small pages -- maybe 4"X4" or so.)  So I feel it\'s a bit over-priced, but it has some fun conversation-starters.  We also use it as a supplement for the game "Loaded Questions".'

    (42)
    'The primary access point in my home office is a Netgear WNDR4000 dual band router.  It has been performing well except when I wanted to take my laptop out on the deck at the other end of the house.  that is why I ordered the Netgear range extender.  That turned out to be a mistake.\n\nThe initial setup requires a direct wired connection which I did using my laptop.  The setup itself was rather easy.  The extender located my primary access point and made a preliminary configuration.  I was then able to remove the cat5 cable and make a wireless connection to customize the configuration using my web browser.  All of that was what I would have expected.\n\nOnce the setup was finished I was able to take the laptop out on the deck where I had a good strong signal. Internet access was fine and I could now access web sites without problems.  The problem started when I attempted to access some of my desktop systems and network attached storage devices in my home office.  I could not locate them using Windows Explorer or other file manager applications.  I don\'t wish to mislead the reader.  I could access other system shares with a file manager if I could remember the IP address and shave name on the remote system  I just could not discover them using the network functions.  This caused a deal breaker problem when I wanted to use the Windows Media Center to watch live TV out on my deck.  Windows MCE could not locate the TV tuners.\n\nIf you don\'t want to do other than surf the web and check e-mail using the extender access point then this is a very fine product.  It was just useless for me because it failed to support the primary function I needed.  That is why I returned it.'

    (40)
    'Not sure how it happened but I ended up with a Sarah Brightman Eden CD. By accident I listened to it and this ole boy liked it. Now when I say I liked it, I mean I really liked it. Now shes  probably my favoite artist. Now I\'m shopping a 2nd Sarah Brightman album. It cant get here soon enough I\'m tellin ya.'
    
    ''' POSTING LIST NUMBERS OFF BY TWO. POSTING LIST SAYS a, ACTUAL LISTING: a + 2
    'Oh, joy! On each disc we are treated to a lecture on the offensiveness of the racial stereotypes that appear in some of the cartoons, courtesy of the sanctimonious Whoopi Goldberg. This from a person whose obscenity laced speech given at a pep rally for Democratic presidential candidate John Kerry was so vulgar that Slim Fast dropped her as a spokesperson for their product. According to an article that appeared in the New York Post, "Whoopi Goldberg delivered an X-rated rant full of sexual innuendoes against President Bush last night at a Radio City gala that raised $7.5 million for the newly minted Democratic ticket of John Kerry and John Edwards. Waving a bottle of wine, she fired off a stream of vulgar sexual wordplays on Bush\'s name in a riff about female genitalia, and boasted that she\'d refused to let Team Kerry clear her material. \'I Xeroxed my behind and I folded it up in an envelope and I sent it back with a big kiss mark on because we\'re Democrats - we\'re not afraid to laugh,\' she said."\n\nI love the cartoons in this set, along with the special features and documentaries on the fine artists who created this classic material. It\'s a shame that Warner Home Video feels compelled to include the hypocritical Goldberg. This set deserves five stars, but Goldberg\'s self-righteous prattling is a major defect.'
    
    'I\'m a huge Sibelius fan, so when they came out with educational software for young children, and when I saw a demo of this, I had to get a copy for my nephews, ages 7 and 3.  Both of them took to this program like I never expected they would.  I got a call from my sister-in-law a few days after I delivered the software, and she was shocked, saying she couldn\'t get the kids off of the computer!  (Finally... something got them away from the X-Box!)  The greatest thing about this program is that it\'s equal learning and fun.  It teaches the basic musical concepts in ways I never thought of, but ways in which today\'s technologically-savvy kids can relate and enjoy.  I have to admit, I had WAY too much fun playing with it myself!  It\'s sophisticated enough for adults to enjoy, but simple enough for kids to understand.  I heard great things about this program on a television review ~  it was a first-place choice for children in a study of educational music software.  Very cool, very fun, very educational.  A great way to get your children started in music!!'
    