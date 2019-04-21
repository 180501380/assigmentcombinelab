import os
import click            #製造command 係透過click呢個插件黎逹成
from app import app


@app.cli.group()              #將呢個decorator decorate 左既function會變成可執行既 父command,你可以係入面加子command,便且係父command 打 --help可以睇到佢有咩 sub command(flask translate --help)
def translate():                #用 flask translate 去執行, 不過呢個function係pass既,所以無野執行既
    """Translation and localization commands."""
    pass


@translate.command()        #@父command.command() decorate左既command會變成可以執行既子command
@click.argument('lang')     #當command要落parameter,就要透過呢個decorator 將parameter傳入返個command度
def init(lang):             #用flask translate init <language code>
    """Initialize a new language."""
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):                 #extract 個pot file,係每次更新翻譯必備,你唔抽啲字出黎,點做翻譯
        raise RuntimeError('extract command failed')                #extract fail會話比你聴
    if os.system(
            'pybabel init -i messages.pot -d app/translations -l ' + lang):
        raise RuntimeError('init command failed')
    os.remove('messages.pot')           #最後會洗返個pot file,因為無次更新翻譯都要行你所起既flask translate init或flask translate update ,command 入面既function都會起過個pot file,所以用完洗左去就得


@translate.command()
def update():               #用flask translate update 去執行
    """Update all languages."""
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):                   #extract 個pot file,係每次更新翻譯必備,你唔抽啲字出黎,點做翻譯
        raise RuntimeError('extract command failed')
    if os.system('pybabel update -i messages.pot -d app/translations'):
        raise RuntimeError('update command failed')
    os.remove('messages.pot')


@translate.command()
def compile():              #用flask translate compile 去執行
    """Compile all languages."""
    if os.system('pybabel compile -d app/translations'):
        raise RuntimeError('compile command failed')

