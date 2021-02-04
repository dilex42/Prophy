import pke
import wikipediaapi


def make_list(key_ph, t=0.5):
    th = key_ph[0][1]* t
    ans = []
    for res in key_ph:
        item = {'phrase':res[0]}
        if res[1] < th :
            break
        page = wiki_wiki.page(f'{res[0]}')
        item['exists'] = page.exists()
        if page.exists() :
            item['title'] = page.title
            page_dis = wiki_wiki.page(f'{page.title}_(disambiguation)')
            dis = page_dis.exists()
            item['dis'] = dis
            if dis :
                item['url'] = page_dis.fullurl
            else :
                item['url'] = page.fullurl
        ans.append(item)
    return ans

        
def extract_keyphrases(caption, n):
    extractor = pke.unsupervised.TextRank()
    extractor.load_document(caption)
    extractor.candidate_selection()
    extractor.candidate_filtering(maximum_word_number=3)
    extractor.candidate_weighting()
    keyphrases = extractor.get_n_best(n=n,redundancy_removal=True)
    if not len(keyphrases):
        return []
    return make_list(keyphrases)


wiki_wiki = wikipediaapi.Wikipedia('en')
