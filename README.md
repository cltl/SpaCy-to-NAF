# SpaCy to NAF

This repository contains everything you need to output SpaCy results in NAF format.

**Example**:

```python
import spacy_to_naf

text = """The cat sat on the mat. Felix was his name."""

NAF = text_to_NAF(text.replace('\n',''))
print(NAF_to_string(NAF))
```

**Output**:
```XML
<NAF>
  <nafHeader>
    <linguisticProcessors layer="text">
      <lp name="SpaCy" timestamp="2015-11-26T15:28:50UTC"/>
    </linguisticProcessors>
    <linguisticProcessors layer="terms">
      <lp name="SpaCy" timestamp="2015-11-26T15:28:50UTC"/>
    </linguisticProcessors>
  </nafHeader>
  <text>
    <wf sent="1" wid="w_0" length="3">The</wf>
    <wf sent="1" wid="w_1" length="3">cat</wf>
    <wf sent="1" wid="w_2" length="3">sat</wf>
    <wf sent="1" wid="w_3" length="2">on</wf>
    <wf sent="1" wid="w_4" length="3">the</wf>
    <wf sent="1" wid="w_5" length="3">mat</wf>
    <wf sent="1" wid="w_6" length="1">.</wf>
    <wf sent="2" wid="w_7" length="5">Felix</wf>
    <wf sent="2" wid="w_8" length="3">was</wf>
    <wf sent="2" wid="w_9" length="3">his</wf>
    <wf sent="2" wid="w_10" length="4">name</wf>
    <wf sent="2" wid="w_11" length="1">.</wf>
  </text>
  <terms>
    <term id="t_0" lemma="the" pos="ADJ" morphofeat="DT">
      <span>
        <!--The-->
        <target id="w_0"/>
      </span>
    </term>
    <term id="t_1" lemma="cat" pos="NOUN" morphofeat="NN">
      <span>
        <!--cat-->
        <target id="w_1"/>
      </span>
    </term>
    <term id="t_2" lemma="sit" pos="VERB" morphofeat="VBD">
      <span>
        <!--sat-->
        <target id="w_2"/>
      </span>
    </term>
    <term id="t_3" lemma="on" pos="ADP" morphofeat="IN">
      <span>
        <!--on-->
        <target id="w_3"/>
      </span>
    </term>
    <term id="t_4" lemma="the" pos="ADJ" morphofeat="DT">
      <span>
        <!--the-->
        <target id="w_4"/>
      </span>
    </term>
    <term id="t_5" lemma="mat" pos="NOUN" morphofeat="NN">
      <span>
        <!--mat-->
        <target id="w_5"/>
      </span>
    </term>
    <term id="t_6" lemma="." pos="PUNCT" morphofeat=".">
      <span>
        <!--.-->
        <target id="w_6"/>
      </span>
    </term>
    <term id="t_7" lemma="felix" pos="NOUN" morphofeat="NNP">
      <span>
        <!--Felix-->
        <target id="w_7"/>
      </span>
    </term>
    <term id="t_8" lemma="be" pos="VERB" morphofeat="VBD">
      <span>
        <!--was-->
        <target id="w_8"/>
      </span>
    </term>
    <term id="t_9" lemma="his" pos="ADJ" morphofeat="PRP$">
      <span>
        <!--his-->
        <target id="w_9"/>
      </span>
    </term>
    <term id="t_10" lemma="name" pos="NOUN" morphofeat="NN">
      <span>
        <!--name-->
        <target id="w_10"/>
      </span>
    </term>
    <term id="t_11" lemma="." pos="PUNCT" morphofeat=".">
      <span>
        <!--.-->
        <target id="w_11"/>
      </span>
    </term>
  </terms>
  <entities>
    <entity id="e_0" type="PERSON">
      <references>
        <span>
          <!--Felix-->
          <target id="t_7"/>
        </span>
      </references>
    </entity>
  </entities>
  <deps>
    <!--det(cat,The)-->
    <dep from="t_1" to="t_0" rfunc="det"/>
    <!--nsubj(sat,cat)-->
    <dep from="t_2" to="t_1" rfunc="nsubj"/>
    <!--prep(sat,on)-->
    <dep from="t_2" to="t_3" rfunc="prep"/>
    <!--det(mat,the)-->
    <dep from="t_5" to="t_4" rfunc="det"/>
    <!--pobj(on,mat)-->
    <dep from="t_3" to="t_5" rfunc="pobj"/>
    <!--punct(sat,.)-->
    <dep from="t_2" to="t_6" rfunc="punct"/>
    <!--nsubj(was,Felix)-->
    <dep from="t_8" to="t_7" rfunc="nsubj"/>
    <!--poss(name,his)-->
    <dep from="t_10" to="t_9" rfunc="poss"/>
    <!--attr(was,name)-->
    <dep from="t_8" to="t_10" rfunc="attr"/>
    <!--punct(was,.)-->
    <dep from="t_8" to="t_11" rfunc="punct"/>
  </deps>
</NAF>
```
