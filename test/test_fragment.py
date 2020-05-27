import sys
#sys.path.insert(0, './Modules/')

import numpy as np

from utils.file_reader import read_file
from utils.fragment_utils import get_fragments
from utils.fragment_encoding import get_encodings, encode_molecule, decode_molecule, encode_list, save_decodings
#from .Modules.models import build_models
#from .Modules.training import train
#from .Modules.rewards import clean_good
from rdkit import rdBase
import logging
logging.getLogger().setLevel(logging.INFO)
rdBase.DisableLog('rdApp.error')


def main(fragment_file, lead_file):
    fragment_mols = read_file(fragment_file)
    lead_mols = read_file(lead_file)
    fragment_mols += lead_mols  #为何要合并？

    logging.info("Read %s molecules for fragmentation library", len(fragment_mols))
    logging.info("Read %s lead moleculs", len(lead_mols))

    #fragment:{fragment_smiles, rdkit.molobj, type(R-group, scaffold, limker)}
    #used_moles不知道为何物
    fragments, used_mols = get_fragments(fragment_mols)
    logging.info("Num fragments: %s", len(fragments))
    logging.info("Total molecules used: %s", len(used_mols))
    assert len(fragments)
    assert len(used_mols)


    encodings, decodings = get_encodings(fragments)
    save_decodings(decodings)
    logging.info("Saved decodings")

    '''
    lead_mols = np.asarray(fragment_mols[-len(lead_mols):])[used_mols[-len(lead_mols):]]
    
    X = encode_list(lead_mols, encodings)
    
    logging.info("Building models")
    actor, critic = build_models(X.shape[1:])

    X = clean_good(X, decodings)

    logging.info("Training")
    history = train(X, actor, critic, decodings)
    logging.info("Saving")
    np.save("History/history.npy", history)
    '''




if __name__ == "__main__":

    #fragment_file = "Data/molecules.smi"
    #lead_file = "Data/dopamineD4props.csv"
    fragment_file = "../utils/data/test_molecules.smi"
    lead_file = "../utils/data/test_dop.csv"

    if len(sys.argv) > 1:
        fragment_file = sys.argv[1]

    if len(sys.argv) > 2:
        lead_file = sys.argv[2]

    main(fragment_file, lead_file)

