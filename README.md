# SpaCy to NAF

This repository contains everything you need to output SpaCy results in NAF format.

Please check **log.md** for updates on the conversion script.

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

## TODO
* add dtd validation of naf version 4
* add https://github.com/huggingface/neuralcoref

**Output**:

Here is the output of the python code above. Please note that the chunks layer
currently only contains PPs and NPs.

```XML
<?xml version='1.0' encoding='utf-8'?>
<NAF xml:lang="en" version="v3.naf">
  <nafHeader>
    <fileDesc creationtime="2019-09-12T11:14:14UTC"/>
    <public/>
    <linguisticProcessors layer="terms">
      <lp beginTimestamp="2019-09-12T11:14:14UTC" endTimestamp="2019-09-12T11:14:14UTC" name="spaCy-model_en_core_web_sm" version="spaCy_version-2.1.4__model_version-2.1.0"/>
    </linguisticProcessors>
    <linguisticProcessors layer="entities">
      <lp beginTimestamp="2019-09-12T11:14:14UTC" endTimestamp="2019-09-12T11:14:14UTC" name="spaCy-model_en_core_web_sm" version="spaCy_version-2.1.4__model_version-2.1.0"/>
    </linguisticProcessors>
    <linguisticProcessors layer="raw">
      <lp beginTimestamp="2019-09-12T11:14:14UTC" endTimestamp="2019-09-12T11:14:14UTC" name="spaCy-model_en_core_web_sm" version="spaCy_version-2.1.4__model_version-2.1.0"/>
    </linguisticProcessors>
    <linguisticProcessors layer="text">
      <lp beginTimestamp="2019-09-12T11:14:14UTC" endTimestamp="2019-09-12T11:14:14UTC" name="spaCy-model_en_core_web_sm" version="spaCy_version-2.1.4__model_version-2.1.0"/>
    </linguisticProcessors>
  </nafHeader>
  <raw>The cat sat on the mat. Felix was his name.</raw>
  <text>
    <wf sent="1" id="w1" length="3" offset="0"><![CDATA[The]]></wf>
    <wf sent="1" id="w2" length="3" offset="4"><![CDATA[cat]]></wf>
    <wf sent="1" id="w3" length="3" offset="8"><![CDATA[sat]]></wf>
    <wf sent="1" id="w4" length="2" offset="12"><![CDATA[on]]></wf>
    <wf sent="1" id="w5" length="3" offset="15"><![CDATA[the]]></wf>
    <wf sent="1" id="w6" length="3" offset="19"><![CDATA[mat]]></wf>
    <wf sent="1" id="w7" length="1" offset="22"><![CDATA[.]]></wf>
    <wf sent="2" id="w8" length="5" offset="24"><![CDATA[Felix]]></wf>
    <wf sent="2" id="w9" length="3" offset="30"><![CDATA[was]]></wf>
    <wf sent="2" id="w10" length="3" offset="34"><![CDATA[his]]></wf>
    <wf sent="2" id="w11" length="4" offset="38"><![CDATA[name]]></wf>
    <wf sent="2" id="w12" length="1" offset="42"><![CDATA[.]]></wf>
  </text>
  <terms>
    <term id="t1" lemma="the" pos="D" type="close" morphofeat="DT">
      <span>
        <target id="w1"/>
      </span>
    </term>
    <term id="t2" lemma="cat" pos="N" type="open" morphofeat="NN">
      <span>
        <target id="w2"/>
      </span>
    </term>
    <term id="t3" lemma="sit" pos="V" type="open" morphofeat="VBD">
      <span>
        <target id="w3"/>
      </span>
    </term>
    <term id="t4" lemma="on" pos="P" type="open" morphofeat="IN">
      <span>
        <target id="w4"/>
      </span>
    </term>
    <term id="t5" lemma="the" pos="D" type="close" morphofeat="DT">
      <span>
        <target id="w5"/>
      </span>
    </term>
    <term id="t6" lemma="mat" pos="N" type="open" morphofeat="NN">
      <span>
        <target id="w6"/>
      </span>
    </term>
    <term id="t7" lemma="." pos="O" type="close" morphofeat=".">
      <span>
        <target id="w7"/>
      </span>
    </term>
    <term id="t8" lemma="Felix" pos="R" type="open" morphofeat="NNP">
      <span>
        <target id="w8"/>
      </span>
    </term>
    <term id="t9" lemma="be" pos="V" type="open" morphofeat="VBD">
      <span>
        <target id="w9"/>
      </span>
    </term>
    <term id="t10" lemma="-PRON-" pos="D" type="close" morphofeat="PRP$">
      <span>
        <target id="w10"/>
      </span>
    </term>
    <term id="t11" lemma="name" pos="N" type="open" morphofeat="NN">
      <span>
        <target id="w11"/>
      </span>
    </term>
    <term id="t12" lemma="." pos="O" type="close" morphofeat=".">
      <span>
        <target id="w12"/>
      </span>
    </term>
  </terms>
  <entities>
    <entity id="e1" type="PERSON">
      <references>
        <span>
          <target id="t7"/>
        </span>
      </references>
      <externalReferences/>
    </entity>
  </entities>
</NAF>
```
