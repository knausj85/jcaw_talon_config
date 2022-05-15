web search <user.dictation>$:         user.web_search(dictation)
(google | goog) <user.dictation>$:    user.google_search(dictation)
bing search <user.dictation>$:        user.bing_search(dictation)
duck duck go <user.dictation>$:       user.duckduckgo_search(dictation)
amazon <user.dictation>$:             user.amazon_search(dictation)
youtube <user.dictation>$:            user.youtube_search(dictation)
reddit <user.dictation>$:             user.reddit_search(dictation)
stack [overflow] <user.dictation>$:   user.stackoverflow_search(dictation)
(wikipedia | wiki) <user.dictation>$: user.wikipedia_search(dictation)
letterboxed <user.dictation>$:        user.letterboxd_search(dictation)
{user.subsearch_site} <user.dictation>$: user.google_subsearch(subsearch_site, dictation)

# Optionally say "plus [whatever]" to add extra stuff to the thing at point
web search [that | thing] [plus <user.dictation>]$:         user.web_search(user.get_that_dwim_plus_text(dictation or ""))
(google | goog) [that | thing] [plus <user.dictation>]$:    user.google_search(user.get_that_dwim_plus_text(dictation or ""))
bing search [that | thing] [plus <user.dictation>]$:        user.bing_search(user.get_that_dwim_plus_text(dictation or ""))
duck duck go [that | thing] [plus <user.dictation>]$:       user.duckduckgo_search(user.get_that_dwim_plus_text(dictation or ""))
amazon [that | thing] [plus <user.dictation>]$:             user.amazon_search(user.get_that_dwim_plus_text(dictation or ""))
youtube [that | thing] [plus <user.dictation>]$:            user.youtube_search(user.get_that_dwim_plus_text(dictation or ""))
reddit [that | thing] [plus <user.dictation>]$:             user.reddit_search(user.get_that_dwim_plus_text(dictation or ""))
stack (overflow | that | thing) [plus <user.dictation>]$:   user.stackoverflow_search(user.get_that_dwim_plus_text(dictation or ""))
(wikipedia | wiki) [that | thing] [plus <user.dictation>]$: user.wikipedia_search(user.get_that_dwim_plus_text(dictation or ""))
{user.subsearch_site} [that | thing] [plus <user.dictation>]$: user.google_subsearch(subsearch_site, user.get_that_dwim_plus_text(dictation or ""))
