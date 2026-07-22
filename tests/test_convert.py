import importlib.util
from pathlib import Path
import pandas as pd
from rdflib import Graph,Literal,URIRef
R=Path(__file__).parents[1];s=importlib.util.spec_from_file_location('c',R/'stages/convert.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def test_n_hexane_canonical_hub(tmp_path):
 row={x:'' for x in ['unii','name','cas_number','ec_number','ncit','rxcui','pubchem_cid','ema_sms_id','epa_dtxsid','molecular_formula','inchikey','smiles','ingredient_type','substance_type']};row.update(unii='2DDG612ED8',name='HEXANE',cas_number='110-54-3',inchikey='VLKZOEOYAKHREP-UHFFFAOYSA-N',smiles='CCCCCC',pubchem_cid='8058',epa_dtxsid='DTXSID0021917')
 p=tmp_path/'x.parquet';pd.DataFrame([row]).to_parquet(p);o=tmp_path/'x.nt';r=m.convert(p,o,tmp_path/'c.json');g=Graph();g.parse(o,format='nt');c=URIRef('https://biobricks.ai/compound/VLKZOEOYAKHREP-UHFFFAOYSA-N');assert r['mapped_cell_coverage']==1;assert (c,m.SMILES,Literal('CCCCCC')) in g and (c,URIRef(m.PROP+'unii'),Literal('2DDG612ED8')) in g
def test_real_source_has_n_hexane():
 p=Path('/mnt/raid2/biobricks/unii-fda/brick/unii_chemicals.parquet')
 if p.exists():assert pd.read_parquet(p,columns=['cas_number']).cas_number.eq('110-54-3').any()
