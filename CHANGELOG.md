# Changelog

<!--next-version-placeholder-->

## v1.1.2 (2022-07-11)
### Documentation
* **README.md:** Change homepage to repository ([`cee904b`](https://github.com/estripling/bumbag/commit/cee904b82e68ffc696bc9dde826df71bdb3aba53))

## v1.1.1 (2022-07-11)
### Documentation
* **DEVELOPERS.md:** Write explicit test section ([`f02a022`](https://github.com/estripling/bumbag/commit/f02a022ceda0c8f236f71d373043210c7f6c9aaf))
* **CONTRIBUTING.md:** Edit get started ([`0605601`](https://github.com/estripling/bumbag/commit/0605601677504335397723a833239d3fbe96ed06))
* ***:** Restructure to add bumbag logo ([`c20088c`](https://github.com/estripling/bumbag/commit/c20088c6c0b2f99adeee7209fbd086cb82b36e06))
* ***:** Move from sphinx-rtd-theme to furo theme ([`aef880f`](https://github.com/estripling/bumbag/commit/aef880f8502e02d386509e1908ef565d1ced08e0))

## v1.1.0 (2022-07-07)
### Feature
* **timestamp:** Prefix archive with timestamp ([`898ddff`](https://github.com/estripling/bumbag/commit/898ddff4e22ea165d02f00f2e35853c0908316d9))
* **io.py:** Add archive_files ([`2a4389f`](https://github.com/estripling/bumbag/commit/2a4389f566d02b8576736704ae32b5fa43f34b47))
* **io.py:** Add query_yes_no ([`270d3ff`](https://github.com/estripling/bumbag/commit/270d3ff7d3858136d64bb8d161de2e182658dc17))
* **random.py:** Add get_random_character ([`2726cbd`](https://github.com/estripling/bumbag/commit/2726cbd97f900585998259f223410f3f877bb4c0))
* **random.py:** Add get_random_integer ([`5726b75`](https://github.com/estripling/bumbag/commit/5726b75d3d9c650eda6ba89fac6e566ad401cfea))
* **random.py:** Add coinflip ([`7769e1f`](https://github.com/estripling/bumbag/commit/7769e1fe8337f10337bc2fe13c202d2340d292ee))
* **random.py:** Add get_random_instance ([`bfa9eeb`](https://github.com/estripling/bumbag/commit/bfa9eebc270ce1a989b05055213ee6f165b431b2))

### Documentation
* **time.py:** Add missing date import in docstring examples ([`a50d5f3`](https://github.com/estripling/bumbag/commit/a50d5f37c3eefa2eb6855a914dd2725548210ddc))
* **example.ipynb:** Add humantime context manager usage example ([`82f0378`](https://github.com/estripling/bumbag/commit/82f03788f4a8b8a4c8b09b812ef283af94ba57f9))
* **example.ipynb:** Improve structure ([`96e32eb`](https://github.com/estripling/bumbag/commit/96e32eb6b08f27ecb92fe51500e7a9e885392988))
* **example.ipynb:** Add dseq usage example - palindrome and ambigram dates ([`1cda8da`](https://github.com/estripling/bumbag/commit/1cda8da5d40eff9c883d2959f59b4998fa65b30c))
* **example.ipynb:** Add complex iseq leap year usage example ([`ca58a68`](https://github.com/estripling/bumbag/commit/ca58a68604d9192edb8dee620dd519b1405015ed))

## v1.0.1 (2022-06-30)
### Fix
* **docs/benchmark_freq_versus_value_counts.py:** Flake8 F401 error ([`737bdd1`](https://github.com/estripling/bumbag/commit/737bdd1623632721bd90ef4deb3b461fc5eb9b64))

### Documentation
* **two_set_summary:** Fix basic set operations link in references ([`7530ae0`](https://github.com/estripling/bumbag/commit/7530ae0ccc4a60f7abb452220d1e4cda5624d5ff))

## v1.0.0 (2022-06-30)
### Feature
* **core.py:** Add freq ([`addccf7`](https://github.com/estripling/bumbag/commit/addccf755f5eebe041eb012cdf68fa9f294dc6b3))

### Breaking
* api change due to refactor  ([`beaf08f`](https://github.com/estripling/bumbag/commit/beaf08f95b7e3534175e4bd21434bcf1e5f141e1))

### Documentation
* **benchmark.md:** Add markdown instead of notebook ([`4112013`](https://github.com/estripling/bumbag/commit/4112013af9db0d7c1449e38632e6daf8de5c2b4d))
* **benchmark.ipynb:** Fix pandas import ([`0f1602a`](https://github.com/estripling/bumbag/commit/0f1602a37e839de6ec1f02db36d0fe87cae02e98))
* **benchmark.ipynb:** Add freq versus value_counts benchmark ([`9ca8ba9`](https://github.com/estripling/bumbag/commit/9ca8ba902fbcbef313735f6f5409dda7cbc6d590))
* **example.ipynb:** Update stopwatch example ([`38edd5a`](https://github.com/estripling/bumbag/commit/38edd5a01a57eca6533b5f2604f2f426f5803c1a))
* **two_set_summary:** Update docstring ([`c8d75f4`](https://github.com/estripling/bumbag/commit/c8d75f43e86f3412b51e9e6f81bbbbabc7f6ad9b))
* **README.md:** Add metadata badge for release ([`31f1939`](https://github.com/estripling/bumbag/commit/31f1939207ec3b7d01a6c9ea617d9b194707509d))

## v0.4.0 (2022-06-19)
### Feature
* **core.py:** Add get_source_code ([`4bd7d86`](https://github.com/estripling/bumbag/commit/4bd7d865da6ac3ce878fb280883e3c074a50fe61))
* **time.py:** Add mseq ([`420e583`](https://github.com/estripling/bumbag/commit/420e583a64187513c0e0dfcca0d21d939d2dc228))
* **time.py:** Add monthrange ([`042d019`](https://github.com/estripling/bumbag/commit/042d019045f7c871c0f638ef46f54965431700e2))
* **time.py:** Add months_between_dates ([`7702c34`](https://github.com/estripling/bumbag/commit/7702c348833e0bf8832f196d9685c7b87baad3fa))
* **time.py:** Add days_between_dates ([`c8be798`](https://github.com/estripling/bumbag/commit/c8be79817ee408afd968acfce55eb60bd048b18b))

### Documentation
* **README.md:** Center title and metadata badges ([`053774e`](https://github.com/estripling/bumbag/commit/053774eb4c1c01a79c62d3e9fd9bae947d4db04d))
* **get_function_name:** Add missing line to doc example ([`929b150`](https://github.com/estripling/bumbag/commit/929b150ae2ba9cdc1422e1db6e7668120e6c806d))
* **remove_punctuation:** Remove type annotation ([`e11b276`](https://github.com/estripling/bumbag/commit/e11b276b859ade18a36fff1c1d38ddc3e0644d50))
* **two_set_summary:** Fix description of show argument ([`51fcb70`](https://github.com/estripling/bumbag/commit/51fcb70e2ddbac12c604081be3a0fd74a79a3633))

## v0.3.0 (2022-06-06)
### Feature
* **time.py:** Add datedelta ([`a687702`](https://github.com/estripling/bumbag/commit/a6877029fcdaf9c066e4e8c1e670b83c5abd8428))
* **math.py:** Add two_set_summary ([`670f126`](https://github.com/estripling/bumbag/commit/670f12628814fcbf9c4e1375f4f9867a028d201a))
* **time.py:** Add dseq ([`b59b721`](https://github.com/estripling/bumbag/commit/b59b7218fa730881382cb6fdb6f3cec9fbfaa864))
* **core.py:** Add date_to_str ([`d67865b`](https://github.com/estripling/bumbag/commit/d67865bca096d4c5e35861b269726a734fa258a1))
* **core.py:** Add str_to_date ([`0acd637`](https://github.com/estripling/bumbag/commit/0acd637f04abc08fb404fd9283cb201cb3e9d43a))
* **core.py:** Add filterregex ([`1624e05`](https://github.com/estripling/bumbag/commit/1624e0515eeb4d1a5c76531bbb20827cf92706b2))
* **core.py:** Add mapregex ([`a192547`](https://github.com/estripling/bumbag/commit/a192547d2016dec042910d10579d6eb082132651))
* **core.py:** Add get_function_name ([`d6e9945`](https://github.com/estripling/bumbag/commit/d6e9945d0d5e2fa1c0d288a9bc5175a012928e64))
* **core.py:** Add extend_range ([`ba52ff5`](https://github.com/estripling/bumbag/commit/ba52ff52f0e16a65f97fef956ce9ee03a1486b50))
* **core.py:** Add sig ([`434436a`](https://github.com/estripling/bumbag/commit/434436acdf3be855eb759a60c26a8a4039fa8422))
* **time.py:** Add humantime ([`6c73d8d`](https://github.com/estripling/bumbag/commit/6c73d8daf4444364b7a951f7d7938cb8aa1ad9ab))
* **math.py:** Add collatz ([`0e75739`](https://github.com/estripling/bumbag/commit/0e75739d3dde4b782ea2b1d12aab79eb25c62d3b))
* **math.py:** Add fibonacci ([`a5a73c6`](https://github.com/estripling/bumbag/commit/a5a73c670a06eb8099c7d3b2e9d1e3dbe18aaac3))
* **math.py:** Add iseq_odd ([`efbe601`](https://github.com/estripling/bumbag/commit/efbe601f152fa322565dd8b6939973601ee135ca))
* **math.py:** Add iseq_even ([`43da052`](https://github.com/estripling/bumbag/commit/43da052ac72c987c9fe5c48166170e163daedc82))
* **math.py:** Add isodd ([`d01180e`](https://github.com/estripling/bumbag/commit/d01180e85deff573b68e3a5dc844da26a4ef79d2))
* **math.py:** Add iseven ([`76dbb21`](https://github.com/estripling/bumbag/commit/76dbb210e7d29a8d57e53a434d9859574df4929c))
* **math.py:** Add iseq ([`203e63b`](https://github.com/estripling/bumbag/commit/203e63b297c656c77693323e76b18f8ccef2ceb7))
* **core.py:** Add op ([`8ea5301`](https://github.com/estripling/bumbag/commit/8ea530107c28f8a3eacfcdc6537caf5d91387187))

### Fix
* **time.py:** Add start-end swap in daterange ([`a1c5837`](https://github.com/estripling/bumbag/commit/a1c58377f591ff90f6281561203de3637f5f7e8e))
* **collatz:** Error message ([`89ee100`](https://github.com/estripling/bumbag/commit/89ee100d73ee7bb8a46e53e2b0abeb9753bddc57))

### Documentation
* **core.py:** Add missing function is curried note ([`38556ed`](https://github.com/estripling/bumbag/commit/38556ed2627059cd7fcbfa68962ad68ba4e28cd4))
* ***:** Fix ISO date statements ([`8d25912`](https://github.com/estripling/bumbag/commit/8d259127a731b7805100647eb9bc75cac5d901d8))
* **README.md:** Change contributing statement ([`fac5fc3`](https://github.com/estripling/bumbag/commit/fac5fc30fc92209e9027c8607d591bd44dab7732))
* **README.md:** Change about statement ([`ddbedaf`](https://github.com/estripling/bumbag/commit/ddbedaf2830cb79c77e29660d84ca61c4497c383))
* **README.md:** Add two_set_summary as usage example ([`f24b8f9`](https://github.com/estripling/bumbag/commit/f24b8f9e9b95227ea25e536afdc20a589dc13000))
* **example.ipynb:** Add two_set_summary as usage example ([`001143d`](https://github.com/estripling/bumbag/commit/001143da21cebadeb2653164bdb1939a36f7caba))
* **example.ipynb:** Add humantime decorator as usage example ([`33151e6`](https://github.com/estripling/bumbag/commit/33151e660e7624eef7989d0d71f01a8e8de3993a))
* **README.md:** Adapt installation instruction ([`dce37d4`](https://github.com/estripling/bumbag/commit/dce37d4a0005666f53e0de6712d31f67dd2f9cdb))
* **time.py:** Change docstring example of daterange ([`6a4f58c`](https://github.com/estripling/bumbag/commit/6a4f58c44bf0e40b3d227cc31c90d1deba3d5fdd))
* **math.py:** Add see also reference to dseq for iseq ([`9eb4798`](https://github.com/estripling/bumbag/commit/9eb4798b72e8fb81f6ae35805edc6793a9915dda))
* **core.py:** Add note that function is curried ([`146385e`](https://github.com/estripling/bumbag/commit/146385e683bd317c922c5debd969e4429937279f))
* **time.py:** Change yields description of daterange ([`9feab63`](https://github.com/estripling/bumbag/commit/9feab632a38ac71cad685e8d511ee6da3084e41c))

## v0.2.0 (2022-06-03)
### Feature
* **time.py:** Add daterange ([`b414f73`](https://github.com/estripling/bumbag/commit/b414f73e198bad9207ab87b5afb4eda74525d081))
* **time.py:** Add is_leap_year ([`9d4ea61`](https://github.com/estripling/bumbag/commit/9d4ea6169e4d68f31ded38136650b1ab4774db12))
* **time.py:** Add get_last_date_of_month ([`40c7088`](https://github.com/estripling/bumbag/commit/40c7088338144fc4618dab08759d227e1d368af8))

## v0.1.0 (2022-05-29)
### Feature
* **core.py:** Add remove_punctuation ([`ac0a615`](https://github.com/estripling/bumbag/commit/ac0a615c8cde2ed682baf3b98cad96c88424b919))

### Documentation
* **README.md:** Add dictionary definition ([`2c5c670`](https://github.com/estripling/bumbag/commit/2c5c6705ad1265a36fcf0fb47258338b5692c613))
* **CHANGELOG.md:** Fix incorrect init logs ([`8ea6498`](https://github.com/estripling/bumbag/commit/8ea649800f14cab66b0e545db1446d5071477ac8))

## v0.0.1 (2022-05-29)
