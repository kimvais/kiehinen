from collections import defaultdict

LANGUAGES = defaultdict(dict)
LANGUAGES[0][0]   = ('n/a',"n/a")
LANGUAGES[10][0]  = ('es', "Spanish")
LANGUAGES[10][16] = ('gt', "Guatemala")
LANGUAGES[10][20] = ('cr', "Costa Rica")
LANGUAGES[10][24] = ('pa', "Panama")
LANGUAGES[10][28] = ('do', "Dominican Republic")
LANGUAGES[10][32] = ('ve', "Venezuela")
LANGUAGES[10][36] = ('co', "Colombia")
LANGUAGES[10][40] = ('pe', "Peru")
LANGUAGES[10][44] = ('ar', "Argentina")
LANGUAGES[10][48] = ('ec', "Ecuador")
LANGUAGES[10][4]  = ('es', "Spain")
LANGUAGES[10][52] = ('cl', "Chile")
LANGUAGES[10][56] = ('uy', "Uruguay")
LANGUAGES[10][60] = ('py', "Paraguay")
LANGUAGES[10][64] = ('bo', "Bolivia")
LANGUAGES[10][68] = ('sv', "El Salvador")
LANGUAGES[10][72] = ('hn', "Honduras")
LANGUAGES[10][76] = ('ni', "Nicaragua")
LANGUAGES[10][80] = ('pr', "Puerto Rico")
LANGUAGES[10][8]  = ('mx', "Mexico")
LANGUAGES[1][0]   = ('ar', "Arabic")
LANGUAGES[11][0]  = ('fi', "Finnish")
LANGUAGES[1][12]  = ('eg', "Egypt")
LANGUAGES[1][20]  = ('dz', "Algeria")
LANGUAGES[12][0]  = ('fr', "French")
LANGUAGES[12][12] = ('ca', "Canada")
LANGUAGES[12][16] = ('ch', "Switzerland")
LANGUAGES[12][20] = ('lu', "Luxembourg")
LANGUAGES[12][24] = ('mc', "Monaco")
LANGUAGES[12][4]  = ('fr', "France")
LANGUAGES[1][24]  = ('ma', "Morocco")
LANGUAGES[12][8]  = ('be', "Belgium")
LANGUAGES[1][28]  = ('tn', "Tunisia")
LANGUAGES[13][0]  = ('he', "Hebrew")
LANGUAGES[1][32]  = ('om', "Oman")
LANGUAGES[1][36]  = ('ye', "Yemen")
LANGUAGES[14][0]  = ('hu', "Hungarian")
LANGUAGES[1][40]  = ('sy', "Syria")
LANGUAGES[1][44]  = ('jo', "Jordan")
LANGUAGES[1][48]  = ('lb', "Lebanon")
LANGUAGES[1][4]   = ('sa', "Saudi Arabia")
LANGUAGES[15][0]  = ('is', "Icelandic")
LANGUAGES[1][52]  = ('kw', "Kuwait")
LANGUAGES[1][56]  = ('ae', "United Arab Emirates")
LANGUAGES[1][60]  = ('bh', "Bahrain")
LANGUAGES[16][0]  = ('it', "Italian")
LANGUAGES[16][4]  = ('it', "Italy")
LANGUAGES[1][64]  = ('qa', "Qatar")
LANGUAGES[16][8]  = ('ch', "Switzerland")
LANGUAGES[17][0]  = ('ja', "Japanese")
LANGUAGES[18][0]  = ('ko', "Korean")
LANGUAGES[19][0]  = ('nl', "Dutch / Flemish")
LANGUAGES[19][8]  = ('be', "Belgium")
#LANGUAGES[1][??] = ('iq', "Iraq) -- Mobipocket broken"
#LANGUAGES[1][??] = ('ly', "Libya) -- Mobipocket broken"
LANGUAGES[20][0]  = ('no', "Norwegian")
LANGUAGES[2][0]   = ('bg', "Bulgarian")
LANGUAGES[21][0]  = ('pl', "Polish")
LANGUAGES[22][0]  = ('pt', "Portuguese")
LANGUAGES[22][4]  = ('br', "Brazil")
LANGUAGES[22][8]  = ('pt', "Portugal")
LANGUAGES[23][0]  = ('rm', "Rhaeto-Romanic")
LANGUAGES[24][0]  = ('ro', "Romanian")
#LANGUAGES[24][??]  = ('mo', "Moldova) (Mobipocket output is 0")
LANGUAGES[25][0]  = ('ru', "Russian")
#LANGUAGES[25][??]  = ('mo', "Moldova) (Mobipocket output is 0")
LANGUAGES[26][0]  = ('hr', "Croatian")
#LANGUAGES[26][12] = ('cyrl', "Cyrillic) (Mobipocket bug")
#LANGUAGES[26][12] = ('latn', "Latin) (Mobipocket bug")
LANGUAGES[26][12] = ('sr', "Serbian")
LANGUAGES[27][0]  = ('sk', "Slovak")
LANGUAGES[28][0]  = ('sq', "Albanian")
LANGUAGES[29][0]  = ('sv', "Swedish")
LANGUAGES[29][8]  = ('fi', "Finland")
LANGUAGES[30][0]  = ('th', "Thai")
LANGUAGES[3][0]   = ('ca', "Catalan")
LANGUAGES[31][0]  = ('tr', "Turkish")
LANGUAGES[32][0]  = ('ur', "Urdu")
LANGUAGES[33][0]  = ('id', "Indonesian")
LANGUAGES[34][0]  = ('uk', "Ukrainian")
LANGUAGES[35][0]  = ('be', "Belarusian")
LANGUAGES[36][0]  = ('sl', "Slovenian")
LANGUAGES[37][0]  = ('et', "Estonian")
LANGUAGES[38][0]  = ('lv', "Latvian")
LANGUAGES[39][0]  = ('lt', "Lithuanian")
LANGUAGES[4][0]   = ('zh', "Chinese")
LANGUAGES[41][0]  = ('fa', "Farsi / Persian")
LANGUAGES[4][12]  = ('hk', "Hong Kong")
LANGUAGES[4][16]  = ('sg', "Singapore")
LANGUAGES[42][0]  = ('vi', "Vietnamese")
LANGUAGES[43][0]  = ('hy', "Armenian")
LANGUAGES[44][0]  = ('az', "Azerbaijani")
#LANGUAGES[44][??] = ('cyrl', ""Cyrillic") -- Mobipocket broken"
#LANGUAGES[44][??] = ('latn', ""Latin") -- Mobipocket broken"
LANGUAGES[4][4]   = ('tw', "Taiwan")
LANGUAGES[45][0]  = ('eu', "Basque")
LANGUAGES[46][0]  = ('sb', "not an IANA language code")
LANGUAGES[47][0]  = ('mk', "Macedonian")
LANGUAGES[48][0]  = ('sx', "not an IANA language code")
LANGUAGES[4][8]   = ('cn', "PRC")
LANGUAGES[49][0]  = ('ts', "Tsonga")
LANGUAGES[50][0]  = ('tn', "Tswana")
LANGUAGES[5][0]   = ('cs', "Czech")
LANGUAGES[52][0]  = ('xh', "Xhosa")
LANGUAGES[53][0]  = ('zu', "Zulu")
LANGUAGES[54][0]  = ('af', "Afrikaans")
LANGUAGES[55][0]  = ('ka', "Georgian")
LANGUAGES[56][0]  = ('fo', "Faroese")
LANGUAGES[57][0]  = ('hi', "Hindi")
LANGUAGES[58][0]  = ('mt', "Maltese")
LANGUAGES[59][0]  = ('sz', "Sami")
LANGUAGES[6][0]   = ('da', "Danish")
LANGUAGES[62][0]  = ('ms', "Malay")
#LANGUAGES[62][??]  = ('bn', "Brunei Darussalam) -- not supported"
#LANGUAGES[62][??]  = ('my', "Malaysia) -- Mobipocket bug"
LANGUAGES[63][0]  = ('kk', "Kazakh")
LANGUAGES[65][0]  = ('sw', "Swahili")
LANGUAGES[67][0]  = ('uz', "Uzbek")
LANGUAGES[67][8]  = ('uz', "Uzbekiztan")
#LANGUAGES[67][??] = ('cyrl', "Cyrillic")
#LANGUAGES[67][??] = ('latn', "Latin")
LANGUAGES[68][0]  = ('tt', "Tatar")
LANGUAGES[69][0]  = ('bn', "Bengali")
LANGUAGES[70][0]  = ('pa', "Punjabi")
LANGUAGES[7][0]   = ('de', "German")
LANGUAGES[71][0]  = ('gu', "Gujarati")
LANGUAGES[7][12]  = ('at', "Austria")
LANGUAGES[7][16]  = ('lu', "Luxembourg")
LANGUAGES[7][20]  = ('li', "Liechtenstein")
LANGUAGES[72][0]  = ('or', "Oriya")
LANGUAGES[73][0]  = ('ta', "Tamil")
LANGUAGES[74][0]  = ('te', "Telugu")
LANGUAGES[75][0]  = ('kn', "Kannada")
LANGUAGES[76][0]  = ('ml', "Malayalam")
LANGUAGES[77][0]  = ('as', "Assamese")
LANGUAGES[78][0]  = ('mr', "Marathi")
LANGUAGES[7][8]   = ('ch', "Switzerland")
LANGUAGES[79][0]  = ('sa', "Sanskrit")
LANGUAGES[8][0]   = ('el', "Greek, Modern (1453-")
LANGUAGES[87][0]  = ('x-kok', "real language code is 'kok'?")
LANGUAGES[9][0]   = ('en', "English")
LANGUAGES[9][12]  = ('au', "Australia")
LANGUAGES[9][16]  = ('ca', "Canada")
LANGUAGES[9][20]  = ('nz', "New Zealand")
LANGUAGES[9][24]  = ('ie', "Ireland")
LANGUAGES[9][28]  = ('za', "South Africa")
LANGUAGES[9][32]  = ('jm', "Jamaica")
LANGUAGES[9][40]  = ('bz', "Belize")
LANGUAGES[9][44]  = ('tt', "Trinidad")
LANGUAGES[9][48]  = ('zw', "Zimbabwe")
LANGUAGES[9][4]   = ('us', "United States")
LANGUAGES[9][52]  = ('ph', "Philippines")
LANGUAGES[97][0]  = ('ne', "Nepali")
LANGUAGES[9][8]   = ('gb', "United Kingdom")
#LANGUAGES[??][??] = ('nb', "Norwegian Bokml (Mobipocket not supported"))
#LANGUAGES[??][??] = ('nn', "Norwegian Nynorsk (Mobipocket not supported"))
