from shutil import move as FileMove
from shutil import copyfile as CopyFile
from pathlib import Path
from subprocess import Popen

def copyToGenerator(filename):
    ''' Moves filename to generator '''
    directory = Path(__file__).parent
    source = directory / filename
    target = directory / 'nona' / filename
    CopyFile(source,target)



def GenerateMultiresOutput(filename):
    ''' Generates the Output folder inside the nona, 
    representing the multiresolution of the given filename image'''
    nonadir = Path(__file__).parent / 'nona'
    x = Popen(['python', 'generate.py', '-n','nona.exe', filename], cwd = nonadir)
    x.wait()


def MoveOutToWeb(panofolderName):
    '''Moves the Output folder from the, OUTPUT FOLDER MUST EXIST
    nona converter to the web with the given name'''
    
    directory = Path(__file__).parent 
    directory / 'downloaded.png'


    outfolder = directory / 'nona' / 'output'
    panofname = directory.parent / 'web' / 'static' / 'panos' / panofolderName

    FileMove(outfolder,panofname)

def GenerateMultiresWrapper(filename, panoFolderOut):
    '''Generates Multires version for the given filename 
    and moves directly into pano folder with the given panoFolderOut name'''
    copyToGenerator(filename)
    GenerateMultiresOutput(filename)
    MoveOutToWeb(panoFolderOut)
