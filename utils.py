{\rtf1\ansi\ansicpg1252\cocoartf1671
{\fonttbl\f0\fnil\fcharset0 Monaco;}
{\colortbl;\red255\green255\blue255;\red192\green192\blue192;\red0\green0\blue255;\red201\green128\blue43;
\red128\green0\blue0;\red0\green170\blue0;}
{\*\expandedcolortbl;;\csgenericrgb\c75294\c75294\c75294;\csgenericrgb\c0\c0\c100000;\csgenericrgb\c78824\c50196\c16863;
\csgenericrgb\c50196\c0\c0;\csgenericrgb\c0\c66667\c0;}
\paperw11900\paperh16840\margl1440\margr1440\vieww10800\viewh8400\viewkind0
\deftab720
\pard\pardeftab720\partightenfactor0

\f0\fs22 \cf2 # -*- coding: \ul utf\ulnone -8 -*-\cf0 \
\
\pard\pardeftab720\partightenfactor0
\cf3 import\cf0  logging\
\cf3 import\cf0  re\
\cf3 try\cf0 :\
    \cf3 from\cf0  urllib \cf3 import\cf0  quote_plus\
    \cf3 from\cf0  urlparse \cf3 import\cf0  urljoin\
\cf3 except\cf0  ImportError:\
    \cf3 from\cf0  urllib.parse \cf3 import\cf0  quote_plus, urljoin\
\
\cf3 import\cf0  requests\
\cf3 from\cf0  bs4 \cf3 import\cf0  BeautifulSoup\
\cf3 from\cf0  requests_futures.sessions \cf3 import\cf0  FuturesSession\
\
\cf3 from\cf0  play_scraper \cf3 import\cf0  settings \cf3 as\cf0  s\
\
log = logging.getLogger(__name__)\
\
\
\cf3 def\cf0  default_headers():\
    \cf3 return\cf0  \{\
        \cf4 'Origin'\cf0 : \cf4 'https://play.google.com'\cf0 ,\
        \cf4 'User-Agent'\cf0 : s.USER_AGENT,\
        \cf4 'Content-Type'\cf0 : \cf4 'application/x-\ul www\ulnone -form-\ul urlencoded\ulnone ;\ul charset\ulnone =UTF-8'\cf0 ,\
    \}\
\
\
\cf3 def\cf0  generate_post_data(results=\cf3 None\cf0 , page=\cf3 None\cf0 , pagtok=\cf3 None\cf0 , children=\cf5 0\cf0 ):\
    \cf4 """\cf0 \
\pard\pardeftab720\partightenfactor0
\cf4     Creates the post data for a POST request. Mainly for pagination and\cf0 \
\cf4     limiting results.\cf0 \
\
\cf4     \cf6 :\ul param\cf4 \ulnone  results: the number of results to return.\cf0 \
\cf4     \cf6 :\ul param\cf4 \ulnone  page: the page number; used to calculate start = page * results.\cf0 \
\cf4     \cf6 :\ul param\cf4 \ulnone  \ul pagtok\ulnone : a page token string for pagination in search.\cf0 \
\cf4     \cf6 :\ul param\cf4 \ulnone  children: number of \ul apps\ulnone  under each collection (used only when\cf0 \
\cf4                      scraping a top-level category's collections).\cf0 \
\cf4     \cf6 :return:\cf4  a dictionary of post data.\cf0 \
\cf4     """\cf0 \
    data = \{\
        \cf4 '\ul ipf\ulnone '\cf0 : \cf5 1\cf0 ,\
        \cf4 '\ul xhr\ulnone '\cf0 : \cf5 1\cf0 \
    \}\
    \cf3 if\cf0  children:\
        data[\cf4 'numChildren'\cf0 ] = children\
    \cf3 if\cf0  results \cf3 is\cf0  \cf3 not\cf0  \cf3 None\cf0 :\
        \cf3 if\cf0  page \cf3 is\cf0  \cf3 not\cf0  \cf3 None\cf0 :\
            start = \cf5 0\cf0  \cf3 if\cf0  page <= \cf5 0\cf0  \cf3 else\cf0  results * page\
            data[\cf4 'start'\cf0 ] = start\
        data[\cf4 '\ul num\ulnone '\cf0 ] = results\
    \cf3 if\cf0  pagtok \cf3 is\cf0  \cf3 not\cf0  \cf3 None\cf0 :\
        data[\cf4 'pagTok'\cf0 ] = pagtok\
    \cf3 return\cf0  data\
\
\
\pard\pardeftab720\partightenfactor0
\cf3 def\cf0  build_url(method, id_string):\
    \cf4 """Creates the absolute \ul url\ulnone  for a type of object. E.g. details, developer,\cf0 \
\pard\pardeftab720\partightenfactor0
\cf4     or similar.\cf0 \
\
\cf4     \cf6 :\ul param\cf4 \ulnone  method: the corresponding method to get for an id.\cf0 \
\cf4     \cf6 :\ul param\cf4 \ulnone  id: an id string query parameter.\cf0 \
\cf4     \cf6 :return:\cf4  a URL string.\cf0 \
\cf4     """\cf0 \
    \cf3 if\cf0  method == \cf4 'developer'\cf0 :\
        id_string = quote_plus(id_string)\
\
    url = \cf4 "\{base\}/\{method\}?id=\{id\}"\cf0 .format(\
        base=s.BASE_URL, method=method, id=id_string)\
    \cf3 return\cf0  url\
\
\
\pard\pardeftab720\partightenfactor0
\cf3 def\cf0  build_collection_url(category=\cf4 ''\cf0 , collection=\cf4 ''\cf0 ):\
    \cf4 """Creates the absolute \ul url\ulnone  based on the category and collection \ul ids\ulnone .\cf0 \
\
\pard\pardeftab720\partightenfactor0
\cf4     \cf6 :\ul param\cf4 \ulnone  category: the category to filter by.\cf0 \
\cf4     \cf6 :\ul param\cf4 \ulnone  collection: the collection to get.\cf0 \
\cf4     \cf6 :return:\cf4  a formatted \ul url\ulnone  string.\cf0 \
\cf4     """\cf0 \
    \cf3 if\cf0  category:\
        category = \cf4 "/category/\{cat\}"\cf0 .format(cat=category)\
    \cf3 if\cf0  collection:\
        collection = \cf4 "/collection/\{\ul col\ulnone \}"\cf0 .format(col=collection)\
\
    url = \cf4 "\{base\}\{category\}\{collection\}"\cf0 .format(\
        base=s.BASE_URL,\
        category=category,\
        collection=collection)\
\
    \cf3 return\cf0  url\
\
\
\pard\pardeftab720\partightenfactor0
\cf3 def\cf0  send_request(method, url, data=\cf3 None\cf0 , params=\cf3 None\cf0 , headers=\cf3 None\cf0 ,\
                 timeout=\cf5 30\cf0 , verify=\cf3 True\cf0 , allow_redirects=\cf3 False\cf0 ):\
    \cf4 """Sends a request to the \ul url\ulnone  and returns the response.\cf0 \
\
\pard\pardeftab720\partightenfactor0
\cf4     \cf6 :\ul param\cf4 \ulnone  method: HTTP method to use.\cf0 \
\cf4     \cf6 :\ul param\cf4 \ulnone  \ul url\ulnone : URL to send.\cf0 \
\cf4     \cf6 :\ul param\cf4 \ulnone  data: Dictionary of post data to send.\cf0 \
\cf4     \cf6 :\ul param\cf4 \ulnone  headers: Dictionary of headers to include.\cf0 \
\cf4     \cf6 :\ul param\cf4 \ulnone  timeout: number of seconds before timing out the request\cf0 \
\cf4     \cf6 :\ul param\cf4 \ulnone  verify: a \ul bool\ulnone  for requesting SSL verification.\cf0 \
\cf4     \cf6 :return:\cf4  a Response object.\cf0 \
\cf4     """\cf0 \
    data = \{\} \cf3 if\cf0  data \cf3 is\cf0  \cf3 None\cf0  \cf3 else\cf0  data\
    params = \{\} \cf3 if\cf0  params \cf3 is\cf0  \cf3 None\cf0  \cf3 else\cf0  params\
    headers = default_headers() \cf3 if\cf0  headers \cf3 is\cf0  \cf3 None\cf0  \cf3 else\cf0  headers\
    \cf3 if\cf0  \cf3 not\cf0  data \cf3 and\cf0  method == \cf4 'POST'\cf0 :\
        data = generate_post_data()\
\
    \cf3 try\cf0 :\
        response = requests.request(\
            method=method,\
            url=url,\
            data=data,\
            params=params,\
            headers=headers,\
            timeout=timeout,\
            verify=verify,\
            allow_redirects=allow_redirects)\
        \cf3 if\cf0  \cf3 not\cf0  response.status_code == requests.codes.ok:\
            response.raise_for_status()\
    \cf3 except\cf0  requests.exceptions.RequestException \cf3 as\cf0  e:\
        log.error(e)\
        \cf3 raise\cf0 \
\
    \cf3 return\cf0  response\
\
\
\pard\pardeftab720\partightenfactor0
\cf3 def\cf0  parse_additional_info(soup):\
    \cf4 """Parses an app's additional information section on its detail page.\cf0 \
\
\pard\pardeftab720\partightenfactor0
\cf4     \cf6 :\ul param\cf4 \ulnone  soup: the additional_info section BeautifulSoup object\cf0 \
\cf4     \cf6 :return:\cf4  a dictionary of the app's parsed additional info\cf0 \
\cf4     """\cf0 \
    \cf2 # This is super ugly because the CSS is obfuscated and doesn't have good\cf0 \
    \cf2 # distinguishing selectors available; each section's \ul markup\ulnone  is nearly\cf0 \
    \cf2 # identical, so we get the values with a similar function.\cf0 \
    section_titles_divs = [x \cf3 for\cf0  x \cf3 in\cf0  soup.select(\cf4 'div.hAyfc div.BgcNfc'\cf0 )]\
\
    title_normalization = \{\
        \cf4 'Updated'\cf0 : \cf4 'updated'\cf0 ,\
        \cf4 'Size'\cf0 : \cf4 'size'\cf0 ,\
        \cf4 'Installs'\cf0 : \cf4 'installs'\cf0 ,\
        \cf4 'Current Version'\cf0 : \cf4 'current_version'\cf0 ,\
        \cf4 'Requires Android'\cf0 : \cf4 'required_android_version'\cf0 ,\
        \cf4 'Content Rating'\cf0 : \cf4 'content_rating'\cf0 ,\
        \cf4 'In-\ul app\ulnone  Products'\cf0 : \cf4 'iap_range'\cf0 ,\
        \cf4 'Interactive Elements'\cf0 : \cf4 'interactive_elements'\cf0 ,\
        \cf4 'Offered By'\cf0 : \cf4 'developer'\cf0 ,\
        \cf4 'Developer'\cf0 : \cf4 'developer_info'\cf0 ,\
    \}\
\
    data = \{\
        \cf4 'updated'\cf0 : \cf3 None\cf0 ,\
        \cf4 'size'\cf0 : \cf3 None\cf0 ,\
        \cf4 'installs'\cf0 : \cf3 None\cf0 ,\
        \cf4 'current_version'\cf0 : \cf3 None\cf0 ,\
        \cf4 'required_android_version'\cf0 : \cf3 None\cf0 ,\
        \cf4 'content_rating'\cf0 : \cf3 None\cf0 ,\
        \cf4 'iap_range'\cf0 : \cf3 None\cf0 ,\
        \cf4 'interactive_elements'\cf0 : \cf3 None\cf0 ,\
        \cf4 'developer'\cf0 : \cf3 None\cf0 ,\
        \cf4 'developer_email'\cf0 : \cf3 None\cf0 ,\
        \cf4 'developer_url'\cf0 : \cf3 None\cf0 ,\
        \cf4 'developer_address'\cf0 : \cf3 None\cf0 ,\
    \}\
\
    \cf3 for\cf0  title_div \cf3 in\cf0  section_titles_divs:\
        section_title = title_div.string\
        \cf3 if\cf0  section_title \cf3 in\cf0  title_normalization:\
            title_key = title_normalization[section_title]\
            value_div = title_div.next_sibling.select_one(\cf4 'span.htlgb'\cf0 )\
\
            \cf3 if\cf0  title_key == \cf4 'content_rating'\cf0 :\
                \cf2 # last string in list is 'Learn more' link\cf0 \
                value = [rating.strip()\
                         \cf3 for\cf0  rating \cf3 in\cf0  value_div.strings][:-\cf5 1\cf0 ]\
            \cf3 elif\cf0  title_key == \cf4 'interactive_elements'\cf0 :\
                value = [ielement.strip()\
                         \cf3 for\cf0  ielement \cf3 in\cf0  value_div.strings]\
            \cf3 elif\cf0  title_key == \cf4 'iap_range'\cf0 :\
                iaps = re.search(\cf4 r'(\\$\\d+\\.\\d\{2\}) - (\\$\\d+\\.\\d\{2\})'\cf0 ,\
                                 value_div.string)\
                \cf3 if\cf0  iaps:\
                    value = iaps.groups()\
            \cf3 elif\cf0  title_key == \cf4 'developer_info'\cf0 :\
                developer_email = value_div.select_one(\cf4 'a[\ul href\ulnone ^="\ul mailto\ulnone :"]'\cf0 )\
                \cf3 if\cf0  developer_email:\
                    developer_email = (developer_email.attrs[\cf4 '\ul href\ulnone '\cf0 ]\
                                                      .split(\cf4 ':'\cf0 )[\cf5 1\cf0 ])\
                developer_url = value_div.select_one(\cf4 'a[\ul href\ulnone ^="\ul http\ulnone "]'\cf0 )\
              \
                \cf3 if\cf0  developer_url:\
                    developer_url = developer_url.attrs[\cf4 '\ul href\ulnone '\cf0 ]\
\
                developer_address = value_div.select(\cf4 '\ul div\ulnone '\cf0 )[-\cf5 1\cf0 ].contents[\cf5 0\cf0 ]\
                \cf3 if\cf0  developer_address.name \cf3 is\cf0  \cf3 not\cf0  \cf3 None\cf0 :\
                    \cf2 # If a bs4 Tag, it will have name attribute, e.g. 'a'\cf0 \
                    \cf2 # Set the address to None for 'not found'\cf0 \
                    \cf2 # The address \ul div\ulnone  should just be a string, no name \ul attr\cf0 \ulnone \
                    developer_address = \cf3 None\cf0 \
                \cf3 if\cf0  developer_address \cf3 is\cf0  \cf3 not\cf0  \cf3 None\cf0 :\
                    developer_address = developer_address.strip()\
\
                \
                developer_pp_address = \cf4 'none'\cf0 \
                \
                \cf3 try\cf0 :\
                    \cf3 for\cf0  t \cf3 in\cf0  value_div.select(\cf4 '\ul div\ulnone '\cf0 ):\
                        \cf3 try\cf0 :\
                            \cf3 if\cf0  t.text == \cf4 'Privacy Policy'\cf0 :\
                                developer_pp_address = value_div.select(\cf4 '\ul div\ulnone '\cf0 )[-\cf5 1\cf0 ].contents[\cf5 0\cf0 ].attrs[\cf4 '\ul href\ulnone '\cf0 ]\
                                \cf3 break\cf0 \
                        \cf3 except\cf0  Exception \cf3 as\cf0  ee:\
                            \cf3 None\cf0 \
                \cf3 except\cf0  Exception \cf3 as\cf0  e:\
                    \cf3 print\cf0  e\
                \cf3 if\cf0  developer_pp_address == \cf4 'none'\cf0 :\
                    \cf3 try\cf0 :\
                        \cf3 for\cf0  t \cf3 in\cf0  value_div.select(\cf4 'a'\cf0 ):\
                            \cf3 try\cf0 :\
                                \cf3 if\cf0  t.text == \cf4 'Privacy Policy'\cf0 :\
                                    developer_pp_address = value_div.select(\cf4 'a'\cf0 )[-\cf5 1\cf0 ].attrs[\cf4 '\ul href\ulnone '\cf0 ]\
                                    \cf3 break\cf0 \
                            \cf3 except\cf0  Exception \cf3 as\cf0  ee:\
                                \cf3 None\cf0 \
                    \cf3 except\cf0  Exception \cf3 as\cf0  e:\
                        \cf3 print\cf0  e\
                \
                \cf3 if\cf0  developer_pp_address == \cf4 'none'\cf0 :\
                    \cf3 print\cf0  \cf4 "no PP for \{0\}"\cf0 .format(value_div)  \
                dev_data = \{\cf4 'developer_email'\cf0 : developer_email,\
                            \cf4 'developer_url'\cf0 : developer_url,\
                            \cf4 'developer_address'\cf0 : developer_address,\
                            \cf4 'developer_pp_address'\cf0 : developer_pp_address\}\
                data.update(dev_data)\
                \cf3 continue\cf0 \
            \cf3 else\cf0 :\
                value = value_div.text\
\
            data[title_key] = value\
    \cf3 return\cf0  data\
\
\
\pard\pardeftab720\partightenfactor0
\cf3 def\cf0  parse_app_details(soup):\
    \cf4 """Extracts an app's details from its info page.\cf0 \
\
\pard\pardeftab720\partightenfactor0
\cf4     \cf6 :\ul param\cf4 \ulnone  soup: a strained BeautifulSoup object of an \ul app\cf0 \ulnone \
\cf4     \cf6 :return:\cf4  a dictionary of \ul app\ulnone  details\cf0 \
\cf4     """\cf0 \
    title = soup.select_one(\cf4 'h1[\ul itemprop\ulnone ="name"] span'\cf0 ).text\
    icon = (soup.select_one(\cf4 '.dQrBL img.ujDFqe'\cf0 )\
                .attrs[\cf4 '\ul src\ulnone '\cf0 ]\
                .split(\cf4 '='\cf0 )[\cf5 0\cf0 ])\
    editors_choice = bool(\
        soup.select_one(\cf4 'meta[\ul itemprop\ulnone ="editorsChoiceBadgeUrl"]'\cf0 ))\
\
    \cf2 # Main category will be first\cf0 \
    category = [c.attrs[\cf4 '\ul href\ulnone '\cf0 ].split(\cf4 '/'\cf0 )[-\cf5 1\cf0 ]\
                \cf3 for\cf0  c \cf3 in\cf0  soup.select(\cf4 'a[\ul itemprop\ulnone ="genre"]'\cf0 )]\
\
    \cf2 # Let the user handle modifying the URL to fetch different resolutions\cf0 \
    \cf2 # Removing the end `=w720-h310-\ul rw\ulnone ` doesn't seem to give original res?\cf0 \
    screenshots = [img.attrs[\cf4 '\ul src\ulnone '\cf0 ]\
                   \cf3 for\cf0  img \cf3 in\cf0  soup.select(\cf4 'button.NIc6yf img.lxGQyd'\cf0 )]\
\
    \cf3 try\cf0 :\
        video = (soup.select_one(\cf4 'button[data-trailer-\ul url\ulnone ^="\ul https\ulnone "]'\cf0 )\
                     .attrs.get(\cf4 'data-trailer-\ul url\ulnone '\cf0 ))\
        \cf3 if\cf0  video \cf3 is\cf0  \cf3 not\cf0  \cf3 None\cf0 :\
            video = video.split(\cf4 '?'\cf0 )[\cf5 0\cf0 ]\
    \cf3 except\cf0  AttributeError:\
        video = \cf3 None\cf0 \
\
    description_soup = soup.select_one(\
        \cf4 '\ul div\ulnone [\ul itemprop\ulnone ="description"] content \ul div\ulnone '\cf0 )\
    \cf3 if\cf0  description_soup:\
        description = \cf4 '\\n'\cf0 .join(description_soup.stripped_strings)\
        description_html = description_soup.encode_contents()\
    \cf3 else\cf0 :\
        description = description_html = \cf3 None\cf0 \
\
    \cf2 # Reviews & Ratings\cf0 \
    \cf3 try\cf0 :\
        score = soup.select_one(\cf4 'div.BHMmbe'\cf0 ).text\
    \cf3 except\cf0  AttributeError:\
        score = \cf3 None\cf0 \
\
    histogram = \{\}\
    \cf3 try\cf0 :\
        reviews = int(soup.select_one(\cf4 'span[\ul aria\ulnone -label$="ratings"]'\cf0 )\
                          .text\
                          .replace(\cf4 ','\cf0 , \cf4 ''\cf0 ))\
        ratings_section = soup.select_one(\cf4 'div.VEF2C'\cf0 )\
        num_ratings = [int(rating.attrs[\cf4 'title'\cf0 ].replace(\cf4 ','\cf0 , \cf4 ''\cf0 ))\
                       \cf3 for\cf0  rating \cf3 in\cf0  ratings_section.select(\
                           \cf4 '\ul div\ulnone  span[style^="width:"]'\cf0 )]\
        \cf3 for\cf0  i \cf3 in\cf0  range(\cf5 5\cf0 ):\
            histogram[\cf5 5\cf0  - i] = num_ratings[i]\
    \cf3 except\cf0  AttributeError:\
        reviews = \cf5 0\cf0 \
\
    \cf3 try\cf0 :\
        changes_soup = soup.select(\cf4 '\ul div\ulnone [\ul itemprop\ulnone ="description"] content'\cf0 )[\cf5 1\cf0 ]\
        recent_changes = \cf4 '\\n'\cf0 .join([x.string.strip() \cf3 for\cf0  x \cf3 in\cf0  changes_soup])\
    \cf3 except\cf0  (IndexError, AttributeError):\
        recent_changes = \cf3 None\cf0 \
\
    \cf3 try\cf0 :\
        price = soup.select_one(\cf4 'meta[\ul itemprop\ulnone ="price"]'\cf0 ).attrs[\cf4 'content'\cf0 ]\
    \cf3 except\cf0  AttributeError:\
        \cf2 # \ul App\ulnone  is probably \ul pre\ulnone -register, requires logged in to see\cf0 \
        \cf3 try\cf0 :\
            price = soup.select_one(\cf4 'not-\ul preregistered\ulnone '\cf0 ).string.strip()\
        \cf3 except\cf0  AttributeError:\
            price = \cf3 None\cf0 \
\
    free = (price == \cf4 '0'\cf0 )\
\
    additional_info_data = parse_additional_info(\
        soup.select_one(\cf4 '.xyOfqd'\cf0 ))\
\
    offers_iap = bool(additional_info_data.get(\cf4 'iap_range'\cf0 ))\
\
    dev_id = soup.select_one(\cf4 'a.hrTbp.R8zArc'\cf0 ).attrs[\cf4 '\ul href\ulnone '\cf0 ].split(\cf4 '='\cf0 )[\cf5 1\cf0 ]\
    developer_id = dev_id \cf3 if\cf0  dev_id \cf3 else\cf0  \cf3 None\cf0 \
\
    data = \{\
        \cf4 'title'\cf0 : title,\
        \cf4 'icon'\cf0 : icon,\
        \cf4 'screenshots'\cf0 : screenshots,\
        \cf4 'video'\cf0 : video,\
        \cf4 'category'\cf0 : category,\
        \cf4 'score'\cf0 : score,\
        \cf4 'histogram'\cf0 : histogram,\
        \cf4 'reviews'\cf0 : reviews,\
        \cf4 'description'\cf0 : description,\
        \cf4 'description_html'\cf0 : description_html,\
        \cf4 'recent_changes'\cf0 : recent_changes,\
        \cf4 'editors_choice'\cf0 : editors_choice,\
        \cf4 'price'\cf0 : price,\
        \cf4 'free'\cf0 : free,\
        \cf4 '\ul iap\ulnone '\cf0 : offers_iap,\
        \cf4 'developer_id'\cf0 : developer_id,\
    \}\
\
    data.update(additional_info_data)\
\
    \cf3 return\cf0  data\
\
\
\pard\pardeftab720\partightenfactor0
\cf3 def\cf0  parse_card_info(soup):\
    \cf4 """Extracts basic \ul app\ulnone  info from the app's card. Used when parsing pages\cf0 \
\pard\pardeftab720\partightenfactor0
\cf4     with lists of \ul apps\ulnone .\cf0 \
\
\cf4     \cf6 :\ul param\cf4 \ulnone  soup: a BeautifulSoup object of an app's card\cf0 \
\cf4     \cf6 :return:\cf4  a dictionary of available basic \ul app\ulnone  info\cf0 \
\cf4     """\cf0 \
    app_id = soup.attrs[\cf4 'data-\ul docid\ulnone '\cf0 ]\
    url = urljoin(s.BASE_URL,\
                  soup.select_one(\cf4 'a.card-click-target'\cf0 ).attrs[\cf4 '\ul href\ulnone '\cf0 ])\
    icon = urljoin(\
        s.BASE_URL,\
        soup.select_one(\cf4 'img.cover-image'\cf0 ).attrs[\cf4 '\ul src\ulnone '\cf0 ].split(\cf4 '='\cf0 )[\cf5 0\cf0 ])\
    title = soup.select_one(\cf4 'a.title'\cf0 ).attrs[\cf4 'title'\cf0 ]\
\
    dev_soup = soup.select_one(\cf4 'a.subtitle'\cf0 )\
    developer = dev_soup.attrs[\cf4 'title'\cf0 ]\
    developer_id = dev_soup.attrs[\cf4 '\ul href\ulnone '\cf0 ].split(\cf4 '='\cf0 )[\cf5 1\cf0 ]\
\
    description = soup.select_one(\cf4 'div.description'\cf0 ).text.strip()\
    score = soup.select_one(\cf4 'div.tiny-star'\cf0 )\
    \cf3 if\cf0  score \cf3 is\cf0  \cf3 not\cf0  \cf3 None\cf0 :\
        score = score.attrs[\cf4 '\ul aria\ulnone -label'\cf0 ].strip().split(\cf4 ' '\cf0 )[\cf5 1\cf0 ]\
\
    \cf3 try\cf0 :\
        price = soup.select_one(\cf4 'span.display-price'\cf0 ).text\
    \cf3 except\cf0  AttributeError:\
        \cf3 try\cf0 :\
            \cf2 # \ul Pre\ulnone -register \ul apps\ulnone  are 'Coming Soon'\cf0 \
            price = soup.select_one(\cf4 'a.price'\cf0 ).text\
        \cf3 except\cf0  AttributeError:\
            \cf2 # Country restricted, no price or buttons shown\cf0 \
            price = \cf3 None\cf0 \
\
    full_price = \cf3 None\cf0 \
    \cf3 if\cf0  price \cf3 is\cf0  \cf3 not\cf0  \cf3 None\cf0 :\
        \cf3 try\cf0 :\
            full_price = soup.select_one(\cf4 'span.full-price'\cf0 ).text\
        \cf3 except\cf0  AttributeError:\
            full_price = \cf3 None\cf0 \
\
    free = (price \cf3 is\cf0  \cf3 None\cf0 )\
    \cf3 if\cf0  free \cf3 is\cf0  \cf3 True\cf0 :\
        price = \cf4 '0'\cf0 \
\
    \cf3 return\cf0  \{\
        \cf4 'app_id'\cf0 : app_id,\
        \cf4 '\ul url\ulnone '\cf0 : url,\
        \cf4 'icon'\cf0 : icon,\
        \cf4 'title'\cf0 : title,\
        \cf4 'developer'\cf0 : developer,\
        \cf4 'developer_id'\cf0 : developer_id,\
        \cf4 'description'\cf0 : description,\
        \cf4 'score'\cf0 : score,\
        \cf4 'full_price'\cf0 : full_price,\
        \cf4 'price'\cf0 : price,\
        \cf4 'free'\cf0 : free\
    \}\
\
\
\pard\pardeftab720\partightenfactor0
\cf3 def\cf0  bg_parse_app_details(session, response):\
    \cf4 """\cf0 \
\pard\pardeftab720\partightenfactor0
\cf4     Requests futures background callback function to asynchronously parse \ul app\cf0 \ulnone \
\cf4     details as the responses are received. Mimics the `details` \ul api\ulnone .\cf0 \
\cf4     """\cf0 \
    \cf3 if\cf0  \cf3 not\cf0  response.status_code == requests.codes.ok:\
        response.raise_for_status()\
    soup = BeautifulSoup(response.content, \cf4 '\ul lxml\ulnone '\cf0 , from_encoding=\cf4 'utf8'\cf0 )\
    details = parse_app_details(soup)\
    response.app_details_data = details\
\
\
\pard\pardeftab720\partightenfactor0
\cf3 def\cf0  multi_futures_app_request(app_ids, headers=\cf3 None\cf0 , verify=\cf3 True\cf0 ,\
                              workers=s.CONCURRENT_REQUESTS):\
    \cf4 """\cf0 \
\pard\pardeftab720\partightenfactor0
\cf4     \cf6 :\ul param\cf4 \ulnone  app_ids: a list of \ul app\ulnone  IDs.\cf0 \
\cf4     \cf6 :\ul param\cf4 \ulnone  headers: a dictionary of custom headers to use.\cf0 \
\cf4     \cf6 :\ul param\cf4 \ulnone  verify: \ul bool\ulnone  for requesting SSL verification.\cf0 \
\cf4     \cf6 :return:\cf4  a list of all \ul apps\ulnone ' detail data\cf0 \
\cf4     """\cf0 \
    session = FuturesSession(max_workers=workers)\
\
    headers = default_headers() \cf3 if\cf0  headers \cf3 is\cf0  \cf3 None\cf0  \cf3 else\cf0  headers\
    responses = [session.get(build_url(\cf4 'details'\cf0 , app_id),\
                             headers=headers,\
                             verify=verify,\
                             background_callback=bg_parse_app_details)\
                 \cf3 for\cf0  app_id \cf3 in\cf0  app_ids]\
\
    apps = []\
    \cf3 for\cf0  i, response \cf3 in\cf0  enumerate(responses):\
        \cf3 try\cf0 :\
            result = response.result()\
            app_json = result.app_details_data\
            app_json.update(\{\
                \cf4 'app_id'\cf0 : app_ids[i],\
                \cf4 '\ul url\ulnone '\cf0 : result.url,\
            \})\
            apps.append(response.result().app_details_data)\
        \cf3 except\cf0  requests.exceptions.RequestException \cf3 as\cf0  e:\
            log.error(\cf4 'Error occurred fetching \{\ul app\ulnone \}'\cf0 .format(app=app_ids[i]))\
\
    \cf3 return\cf0  apps\
}