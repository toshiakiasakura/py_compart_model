from setuptools import setup
from codecs import open
from os import path

current = path.abspath(path.dirname(__file__))

# long_description(後述)に、GitHub用のREADME.mdを指定
with open(path.join(current, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='py_compart_model', # パッケージ名(プロジェクト名)
    packages=['py_compart_model'], # パッケージ内(プロジェクト内)のパッケージ名をリスト形式で指定

    # version='0.1.1', # バージョン -> setup.cfg

    license='MIT', # ライセンス

    install_requires=['scipy', 'matplotlib'], # pip installする際に同時にインストールされるパッケージ名をリスト形式で指定

    author='toshiakiasakura', # パッケージ作者の名前
    author_email='wordpress.akitoshi@gmail.com', # パッケージ作者の連絡先メールアドレス
    url='https://github.com/toshiakiasakura/py_compart_model', # パッケージに関連するサイトのURL(GitHubなど)

    description='User friendly syntax of compartment model, especially dedicated to epidemiological models.', # パッケージの簡単な説明
    long_description=long_description, # PyPIに'Project description'として表示されるパッケージの説明文
    long_description_content_type='text/markdown', # long_descriptionの形式を'text/plain', 'text/x-rst', 'text/markdown'のいずれかから指定
    keywords='compartment epidemiology solve_ivp ODE population dynammics', # PyPIでの検索用キーワードをスペース区切りで指定

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ], # パッケージ(プロジェクト)の分類。https://pypi.org/classifiers/に掲載されているものを指定可能。
)

