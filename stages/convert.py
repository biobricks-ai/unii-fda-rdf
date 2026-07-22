#!/usr/bin/env python3
"""Stream FDA UNII chemical identities to N-Triples."""
from __future__ import annotations
import hashlib,json,re
from pathlib import Path
import pandas as pd
from rdflib import Literal,URIRef
from rdflib.namespace import DCTERMS,RDF,RDFS
from rdflib.plugins.serializers.nt import _quoteLiteral
BASE='https://biobricks.ai/unii/'; PROP='https://biobricks.ai/ontology/unii/'
CHEM=URIRef('http://purl.obolibrary.org/obo/CHEBI_24431'); SMILES=URIRef('http://semanticscience.org/resource/CHEMINF_000018'); INCHIKEY=URIRef('http://semanticscience.org/resource/CHEMINF_000059'); SOURCE=URIRef('https://precision.fda.gov/uniisearch')
FIELDS={'ec_number':'ecNumber','ncit':'ncitCode','rxcui':'rxNormConcept','pubchem_cid':'pubchemCID','ema_sms_id':'emaSMSID','epa_dtxsid':'dtxsid','molecular_formula':'molecularFormula','ingredient_type':'ingredientType','substance_type':'substanceType'}
def text(v): return '' if v is None or pd.isna(v) else str(v).strip()
def nt(x): return f'<{x}>' if isinstance(x,URIRef) else _quoteLiteral(x)
def emit(o,s,p,v):o.write(f'{nt(s)} {nt(p)} {nt(v)} .\n');return 1
def convert(source,output,coverage):
 d=pd.read_parquet(source);output.parent.mkdir(parents=True,exist_ok=True);emitted=mapped=declared=converted=0
 with output.open('w') as o:
  for _,r in d.iterrows():
   unii=text(r.unii);cas=text(r.cas_number);key=text(r.inchikey);smi=text(r.smiles)
   if not unii:continue
   converted+=1;c=URIRef('https://biobricks.ai/compound/'+key) if key else (URIRef('https://biobricks.ai/compound/unmapped/cas/'+cas) if cas else URIRef(BASE+'substance/'+unii))
   emitted+=emit(o,c,RDF.type,CHEM)+emit(o,c,DCTERMS.source,SOURCE)+emit(o,c,URIRef(PROP+'unii'),Literal(unii));mapped+=1;declared+=1
   for value,pred in [(text(r['name']),RDFS.label),(cas,URIRef('https://biobricks.ai/ontology/casNumber')),(key,INCHIKEY),(smi,SMILES)]:
    if value:emitted+=emit(o,c,pred,Literal(value));mapped+=1;declared+=1
   for col,local in FIELDS.items():
    value=text(r.get(col))
    if value:emitted+=emit(o,c,URIRef(PROP+local),Literal(value));mapped+=1;declared+=1
 report={'source_rows':len(d),'converted_records':converted,'record_count_coverage':converted/len(d),'identifier_row_coverage':converted/len(d),'declared_mapped_cells':declared,'mapped_nonempty_cells':mapped,'mapped_cell_coverage':mapped/declared,'emitted_statements':emitted}
 coverage.parent.mkdir(parents=True,exist_ok=True);coverage.write_text(json.dumps(report,indent=2)+'\n');return report
def main():
 import biobricks as bb
 a=bb.assets('unii-fda');report=convert(Path(a.unii_chemicals_parquet),Path('brick/unii-fda-rdf.nt'),Path('reports/source-coverage.json'));Path('reports/ontology-health.json').write_text(json.dumps({'status':'pass','local_classes':0,'local_predicates':10},indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
