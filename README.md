# SpaCy to NAF

This repository contains everything you need to output SpaCy results in NAF format.


**Example**:

```python
import spacy_to_naf
import spacy

nlp = spacy.load('en')

text = """The cat sat on the mat. Felix was his name."""

NAF = spacy_to_naf.text_to_NAF(text, nlp)
print(spacy_to_naf.NAF_to_string(NAF))
```

Or use the command line:
```
python spacy_to_naf.py example_files/felix.txt > example_files/felix.naf
```

NB. Don't use this for batch processing! That would mean loading SpaCy for each
file, which is wildly inefficient. For large batches, write a python script that
loads SpaCy and this module, loops over the files, and writes out NAF in one go.

**Output**:

Here is the output of the python code above. Please note that the chunks layer
currently only contains PPs and NPs.

```XML
<?xml version='1.0' encoding='utf-8'?>
<NAF xml:lang="en" version="v3.naf">
  <nafHeader>
    <linguisticProcessors layer="text">
      <lp name="spaCy-2.0.0_model-core_web_sm" timestamp="2019-06-13T10:04:46UTC"/>
    </linguisticProcessors>
    <linguisticProcessors layer="raw">
      <lp name="spaCy-2.0.0_model-core_web_sm" timestamp="2019-06-13T10:04:46UTC"/>
    </linguisticProcessors>
    <linguisticProcessors layer="entities">
      <lp name="spaCy-2.0.0_model-core_web_sm" timestamp="2019-06-13T10:04:46UTC"/>
    </linguisticProcessors>
    <linguisticProcessors layer="terms">
      <lp name="spaCy-2.0.0_model-core_web_sm" timestamp="2019-06-13T10:04:46UTC"/>
    </linguisticProcessors>
  </nafHeader>
  <raw>The cat sat on the mat. Felix was his name.</raw>
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
    <term id="t0" lemma="the" pos="DET" morphofeat="DT">
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
    <term id="t4" lemma="the" pos="DET" morphofeat="DT">
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
    <term id="t7" lemma="felix" pos="PROPN" morphofeat="NNP">
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
    <term id="t9" lemma="-PRON-" pos="ADJ" morphofeat="PRP$">
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
  <entities/>
</NAF>
```
