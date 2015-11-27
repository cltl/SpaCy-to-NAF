# SpaCy to NAF

This repository contains everything you need to output SpaCy results in NAF format.

**Example**:

```python
import spacy_to_naf
from spacy.en import English

nlp = English()

text = """The cat sat on the mat. Felix was his name."""

NAF = spacy_to_naf.text_to_NAF(text, nlp)
print(spacy_to_naf.NAF_to_string(NAF))
```

Or use the command line:
```
python spacy_to_naf.py felix.txt > felix.naf
```

**Output**:
```XML
<NAF>
  <nafHeader>
    <linguisticProcessors layer="text">
      <lp name="SpaCy" timestamp="2015-11-26T17:21:54UTC"/>
    </linguisticProcessors>
    <linguisticProcessors layer="terms">
      <lp name="SpaCy" timestamp="2015-11-26T17:21:54UTC"/>
    </linguisticProcessors>
  </nafHeader>
  <text>
    <wf sent="1" id="w0" length="3" offset="0">The</wf>
    <wf sent="1" id="w1" length="3" offset="4">cat</wf>
    <wf sent="1" id="w2" length="3" offset="8">sat</wf>
    <wf sent="1" id="w3" length="2" offset="12">on</wf>
    <wf sent="1" id="w4" length="3" offset="15">the</wf>
    <wf sent="1" id="w5" length="3" offset="19">mat</wf>
    <wf sent="1" id="w6" length="1" offset="22">.</wf>
    <wf sent="2" id="w7" length="5" offset="24">Felix</wf>
    <wf sent="2" id="w8" length="3" offset="30">was</wf>
    <wf sent="2" id="w9" length="3" offset="34">his</wf>
    <wf sent="2" id="w10" length="4" offset="38">name</wf>
    <wf sent="2" id="w11" length="1" offset="42">.</wf>
  </text>
  <terms>
    <term id="t0" lemma="the" pos="ADJ" morphofeat="DT">
      <span>
        <!--The-->
        <target id="w0"/>
      </span>
    </term>
    <term id="t1" lemma="cat" pos="NOUN" morphofeat="NN">
      <span>
        <!--cat-->
        <target id="w1"/>
      </span>
    </term>
    <term id="t2" lemma="sit" pos="VERB" morphofeat="VBD">
      <span>
        <!--sat-->
        <target id="w2"/>
      </span>
    </term>
    <term id="t3" lemma="on" pos="ADP" morphofeat="IN">
      <span>
        <!--on-->
        <target id="w3"/>
      </span>
    </term>
    <term id="t4" lemma="the" pos="ADJ" morphofeat="DT">
      <span>
        <!--the-->
        <target id="w4"/>
      </span>
    </term>
    <term id="t5" lemma="mat" pos="NOUN" morphofeat="NN">
      <span>
        <!--mat-->
        <target id="w5"/>
      </span>
    </term>
    <term id="t6" lemma="." pos="PUNCT" morphofeat=".">
      <span>
        <!--.-->
        <target id="w6"/>
      </span>
    </term>
    <term id="t7" lemma="felix" pos="NOUN" morphofeat="NNP">
      <span>
        <!--Felix-->
        <target id="w7"/>
      </span>
    </term>
    <term id="t8" lemma="be" pos="VERB" morphofeat="VBD">
      <span>
        <!--was-->
        <target id="w8"/>
      </span>
    </term>
    <term id="t9" lemma="his" pos="ADJ" morphofeat="PRP$">
      <span>
        <!--his-->
        <target id="w9"/>
      </span>
    </term>
    <term id="t10" lemma="name" pos="NOUN" morphofeat="NN">
      <span>
        <!--name-->
        <target id="w10"/>
      </span>
    </term>
    <term id="t11" lemma="." pos="PUNCT" morphofeat=".">
      <span>
        <!--.-->
        <target id="w11"/>
      </span>
    </term>
  </terms>
  <entities>
    <entity id="e0" type="PERSON">
      <references>
        <span>
          <!--Felix-->
          <target id="t7"/>
        </span>
      </references>
    </entity>
  </entities>
  <deps>
    <!--det(cat,The)-->
    <dep from="t1" to="t0" rfunc="det"/>
    <!--nsubj(sat,cat)-->
    <dep from="t2" to="t1" rfunc="nsubj"/>
    <!--prep(sat,on)-->
    <dep from="t2" to="t3" rfunc="prep"/>
    <!--det(mat,the)-->
    <dep from="t5" to="t4" rfunc="det"/>
    <!--pobj(on,mat)-->
    <dep from="t3" to="t5" rfunc="pobj"/>
    <!--punct(sat,.)-->
    <dep from="t2" to="t6" rfunc="punct"/>
    <!--nsubj(was,Felix)-->
    <dep from="t8" to="t7" rfunc="nsubj"/>
    <!--poss(name,his)-->
    <dep from="t10" to="t9" rfunc="poss"/>
    <!--attr(was,name)-->
    <dep from="t8" to="t10" rfunc="attr"/>
    <!--punct(was,.)-->
    <dep from="t8" to="t11" rfunc="punct"/>
  </deps>
</NAF>
```
