# Project
## Properties

- client : ACME
- project_name : ACME Pentest
- start_date : 01/01/1970
- end_date : 07/01/1970

## Contacts

| Name        | Function    | Mail                 | Phone      |
|:------------|:------------|:---------------------|:-----------|
| John Smith  | Lorem       | john.smith@acme.com  | 0123456789 |
| Bob Smith   | Ipsum       | bob.smith@acme.com   | 0123456789 |
| Alice Smith | Consectetur | alice.smith@acme.com | 0123456789 |

## Auditors

| Name      | *Function*    | Mail                | Phone      |
|:----------|:--------------|:--------------------|:-----------|
| John Doe  | Porttitor     | john.doe@wayne.com  | 0123456789 |
| Bob Doe   | Sed bibendum  | bob.doe@wayne.com   | 0123456789 |
| Alice Doe | Massa commodo | alice.doe@wayne.com | 0123456789 |

## Scope

| Name      | DNS             | IP        |
|:----------|:----------------|:----------|
| Example 1 | *example.com*   | 127.0.0.1 |
| Example 2 | **example.com** | 127.0.0.2 |
| Example 3 | ~~example.com~~ | 127.0.0.3 |

## Description

Lorem ipsum dolor sit **amet**, *consectetur* ~~adipiscing elit~~.
Sed sit amet sapien et tortor interdum semper in sed purus. 
Ut auctor gravida leo et mattis. 

## Synthesis

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed sit amet sapien et tortor interdum semper in sed purus. Ut auctor gravida leo et mattis. Morbi ipsum sapien, dignissim vitae convallis nec, blandit vitae enim. Nulla rhoncus diam et sem rhoncus sodales. Donec imperdiet lectus augue. Integer quis lacus in justo malesuada accumsan ac ut tellus. Pellentesque efficitur maximus tellus, vel vestibulum neque varius in. Aliquam dapibus lectus vitae ex ultricies, quis laoreet orci aliquet. Integer efficitur massa in tempus mollis. Etiam dictum, dui ac posuere pulvinar, risus quam eleifend eros, non vulputate ante lorem eget enim.
Ut convallis mi dui, at ultricies mi faucibus quis. Donec pretium bibendum tellus, in mollis ligula imperdiet et. Nulla at ex suscipit, egestas sapien nec, eleifend ligula. Ut efficitur mi sodales nunc iaculis, sed consectetur tellus efficitur. Praesent quis lectus enim. Vivamus vel euismod libero. Suspendisse sodales pulvinar interdum. Cras non magna tincidunt, vehicula justo in, consectetur lectus. Proin mollis neque nec tincidunt feugiat. In in egestas diam, et finibus eros. Quisque sit amet tincidunt turpis.
Mauris in purus gravida, dictum magna sit amet, pulvinar risus. In libero ipsum, sodales at rhoncus vitae, pharetra id mi. Aenean eu nibh ligula. Nam mollis odio in elit bibendum mollis. Aenean non augue at justo bibendum imperdiet. Etiam maximus sed ex nec tincidunt. Morbi at rutrum risus. Aliquam ligula nisl, interdum vitae ipsum in, mattis dapibus justo.
Etiam eleifend malesuada massa. Vestibulum accumsan molestie feugiat. Ut ante nibh, pellentesque non consequat id, lobortis finibus massa. Nulla sed ornare mi. Cras velit ipsum, lobortis ac venenatis id, luctus nec diam. In hac habitasse platea dictumst. Nullam vitae tincidunt est, vel finibus lorem. Pellentesque iaculis sem et maximus gravida. Donec sit amet commodo erat.

# Vulnerabilities
## XSS
### Properties

- name: XSS
- id: VULN-01
- severity: Medium
- cvss : 3.1 AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:L

### Description

Lorem ipsum dolor sit amet, consectetur adipiscing elit. In quis fringilla diam. Integer turpis eros, venenatis vel fermentum sit amet, efficitur non leo. Etiam bibendum pretium sapien eu facilisis. In tristique magna et massa aliquam feugiat. Interdum et malesuada fames ac ante ipsum primis in faucibus. Duis auctor nunc quis diam aliquam tempor. Nullam varius sodales magna. Sed placerat auctor eros ac aliquet. 

Lorem ipsum dolor sit amet :
1. Lorem ipsum dolor sit amet *Cras fringilla elit sed purus tempus*
    1. Lorem ipsum dolor sit amet **Cras fringilla elit sed purus tempus**
        1. Lorem ipsum dolor sit amet ~~Cras fringilla elit sed purus tempus~~
            1. Lorem ipsum dolor sit amet 

### Test

Phasellus facilisis dapibus interdum. Sed eget lacinia justo, non facilisis dui. Nulla facilisi.

```
Nam scelerisque luctus nibh. Sed nec elementum leo. Etiam eu urna non eros euismod congue. Aenean non risus vehicula, aliquam lacus vitae, sodales metus. Donec tincidunt nisl ut turpis gravida sodales. Aliquam sit amet ornare augue. Phasellus tristique tellus nec ante lacinia, ut facilisis augue volutpat. Nunc sodales ullamcorper lorem eu suscipit. Cras odio tortor, consectetur nec volutpat id, sagittis sed sem. Ut ultrices placerat interdum. Sed odio arcu, elementum in lobortis sed, blandit ut risus. Vivamus lobortis, ipsum et sollicitudin auctor, diam lorem euismod turpis, ut placerat quam augue a ante. Nam dapibus ligula neque.
```

Lorem ipsum dolor sit amet, consectetur adipiscing elit : `In quis fringilla diam. Integer turpis eros`

### Remediation

Filter user input and encode data output

[](https://www.example.com)

## RCE
### Properties

- name: RCE
- id: VULN-02
- severity: Critical
- cvss : 3.1 AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:L

### Description

Donec vulputate lacinia nibh, eget tempor enim aliquam et. Maecenas eleifend leo eu justo congue iaculis.

Sed sit amet lorem ac ipsum tincidunt sodales in non dui.:
- Vivamus efficitur tellus sapien.
- Nunc auctor, lectus vitae blandit egestas.
- Nunc consequat magna lorem.
    + Vivamus efficitur tellus sapien
    + ac vestibulum turpis sodales eget
        * Phasellus facilisis dapibus interdum
        * Sed eget lacinia justo, non facilisis dui
            - Quisque aliquet ullamcorper ante
            - Proin quis turpis efficitur
                + Nullam lectus elit
                + molestie et euismod volutpat

### Test

Etiam sed euismod mi, vitae bibendum sapien. Nullam non augue porttitor, varius tellus quis:

```javascript
var search = document.getElementById('search').value;
var results = %%`document.getElementById('results');%%`
results.innerHTML = 'You searched for: ' + search;
```

| IP      | PORT         |
|:----------|:------------|
| 127.0.0.1 | 22 |
| 127.0.0.2 | 80 | 
| 127.0.0.3 | 80, 443 |

![xxs.jpg](img\xss.jpg)

Nulla elementum rhoncus quam `Orci varius natoque penatibus` eget maximus ligula lacinia dignissim.

### Remediation

Ut sed ipsum elit. Proin bibendum porttitor viverra

[Mauris consequat metus **in nibh gravida iaculis**](https://www.example.com)
