# Annotation Loaders

{% for annot_ldr in annotation_loaders %}
## {{ annot_ldr.name|markdown }}

{{ annot_ldr.description|markdown }}

### Parameters

{% for parameter in annot_ldr.parameters %}
**{{parameter.name|markdown}}** *({{parameter.type|markdown}})*{% if parameter.required %}, required{% else %} = {{parameter.default|markdown}}{%endif%}<br/>
{{parameter.description|markdown}}

{% for ensure in parameter.ensures %}
* {{ensure|markdown}}
{% endfor %}
{% endfor %}

{% if annot_ldr.ensures %}
#### Other Conditions


{% for ensure in annot_ldr.ensures %}
* {{ ensure|markdown }}
{% endfor %}
{% endif %}

{% endfor %}

# Annotation Writers

{% for annot_wtr in annotation_writers %}
## {{ annot_wtr.name|markdown }}

{{ annot_wtr.description|markdown }}

### Parameters

{% for parameter in annot_wtr.parameters %}
**{{parameter.name|markdown}}** *({{parameter.type|markdown}})*{% if parameter.required %}, required{% else %} = {{parameter.default|markdown}}{%endif%}<br/>
{{parameter.description|markdown}}

{% for ensure in parameter.ensures %}
* {{ensure|markdown}}
{% endfor %}
{% endfor %}

{% if annot_wtr.ensures %}
#### Other Conditions

{% for ensure in annot_wtr.ensures %}
* {{ ensure|markdown }}
{% endfor %}
{% endif %}

{% endfor %}

# Image Loaders

{% for image_ldr in image_loaders %}
## {{ image_ldr.name|markdown }}

{{ image_ldr.description|markdown }}

### Parameters

{% for parameter in image_ldr.parameters %}
**{{parameter.name|markdown}}** *({{parameter.type|markdown}})*{% if parameter.required %}, required{% else %} = {{parameter.default|markdown}}{%endif%}<br/>
{{parameter.description|markdown}}

{% for ensure in parameter.ensures %}
* {{ensure|markdown}}
{% endfor %}
{% endfor %}

{% if image_ldr.ensures %}
#### Other Conditions

{% for ensure in image_ldr.ensures %}
* {{ ensure|markdown }}
{% endfor %}
{% endif %}

{% endfor %}

# Image Writers

{% for image_wtr in image_writers %}
## {{ image_wtr.name|markdown }}

{{ image_wtr.description|markdown }}

### Parameters

{% for parameter in image_wtr.parameters %}
**{{parameter.name|markdown}}** *({{parameter.type|markdown}})*{% if parameter.required %}, required{% else %} = {{parameter.default|markdown}}{%endif%}<br/>
{{parameter.description|markdown}}

{% for ensure in parameter.ensures %}
* {{ensure|markdown}}
{% endfor %}
{% endfor %}

{% if image_wtr.ensures %}
#### Other Conditions

{% for ensure in image_wtr.ensures %}
* {{ ensure|markdown }}
{% endfor %}
{% endif %}

{% endfor %}

# Augmentations

{% for augmentation in augmentations %}
## {{ augmentation.name|markdown }}

{{ augmentation.description|markdown }}

### Example
<table style="width: 100%">
<tr>
<td><b>Input Image</b></td>
<td><b>Augmented Image</b></td>
<td><b>Input Image<br/>(with Bounding Boxes)</b></td>
<td><b>Augmented Image<br/>(with Bounding Boxes)</b></td>
</tr>
<tr>
<td style="vertical-align: bottom">
<img src="{{image_root}}{{ augmentation.sample_image }}" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="{{image_root}}{{ augmentation.augmented_image }}" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="{{image_root}}{{ augmentation.sample_image_bboxes }}" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="{{image_root}}{{ augmentation.augmented_image_bboxes }}" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

</tr>
</table>

### Parameters

{% for parameter in augmentation.parameters %}
**{{parameter.name|markdown}}** *({{parameter.type|markdown}})*{% if parameter.required %}, required{% else %} = {{parameter.default|markdown}}{%endif%}<br/>
{{parameter.description|markdown}}

{% for ensure in parameter.ensures %}
* {{ensure|markdown}}
{% endfor %}
{% endfor %}

{% if augmentation.sample_options %}
Sample image augmented with options:
```
{{augmentation.sample_options}}```
{% endif %}

{% if augmentation.ensures %}
#### Other Conditions

{% for ensure in augmentation.ensures %}
* {{ ensure|markdown }}
{% endfor %}
{% endif %}

{% endfor %}
