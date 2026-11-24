# Third-Party Licenses & Open-Source Notices

This product (`bibi`) is based on the open-source project **Pip-KeyPet** (`Copyright (c) 2026 David Novikov`, MIT License — <https://github.com/NovikovVisuals/Pip-KeyPet>) and incorporates the third-party open-source components listed below.

> **FreeType Project Credit:**
> Portions of this software are copyright © 2026 The FreeType Project (<https://freetype.org>). All rights reserved.

---

## Summary of Components

| Component | Version | License | Copyright / Author |
| --- | --- | --- | --- |
| **Pip-KeyPet** (upstream base) | 1.2.0 | MIT | Copyright (c) 2026 David Novikov |
| **ESP-IDF** | 5.5.x | Apache-2.0 (core) / MIT / BSD | Espressif Systems (Shanghai) Co., Ltd. |
| **Espressif IDF Components** (`button` 4.2.1, `cmake_utilities` 0.5.3, `esp_codec_dev` 1.5.11, `esp_io_expander` 1.2.1, `esp_lcd_co5300` 2.2.0, `esp_lcd_panel_io_additions` 1.0.1~1, `esp_lcd_touch` 1.2.1, `esp_lvgl_adapter` 0.6.4, `esp_lv_decoder` 0.4.3, `esp_lv_fs` 1.0.1, `esp_mmap_assets` 2.0.1, `knob` 1.1.0) | see `firmware/dependencies.lock` | Apache-2.0 | Espressif Systems (Shanghai) Co., Ltd. |
| **Waveshare BSP** (`waveshare/esp32_s3_touch_amoled_1_75c`) | 3.0.0 | Apache-2.0 | Waveshare Electronics |
| **Waveshare Touch Driver** (`waveshare/esp_lcd_touch_cst9217`) | 2.0.0 | Apache-2.0 | Waveshare Electronics |
| **esptool-js** (web flasher) | 0.6.1 | Apache-2.0 | Espressif Systems (Shanghai) Co., Ltd. |
| **Material Symbols Rounded** (web UI icons) | Google Fonts | Apache-2.0 | Google LLC |
| **espressif/esp_new_jpeg** | 1.0.2 | ESPRESSIF MIT (Espressif products only) | Copyright (c) 2024 Espressif Systems (Shanghai) Co., Ltd. |
| **LVGL** (`lvgl/lvgl`) | 9.5.0 | MIT | Copyright (c) 2025 LVGL Kft |
| **Project Nayuki QR Code Generator** (bundled in LVGL) | in LVGL 9.5.0 | MIT | Copyright © 2025 Project Nayuki |
| **Three.js** (web simulator) | 0.170.0 | MIT | Copyright © 2010-2024 three.js authors |
| **FreeType** (`espressif/freetype`) | 2.14.3~1 | FreeType License (FTL) | Copyright 1996-2002, 2006 David Turner, Robert Wilhelm, and Werner Lemberg |
| **libpng** (`espressif/libpng`) | 1.6.58~2 | PNG Reference Library License v2 | Copyright (c) 1995-2019 The PNG Reference Library Authors |
| **zlib** (`espressif/zlib`) | 1.3.2~1 | Zlib License | Copyright (C) 1995-2022 Jean-loup Gailly and Mark Adler |
| **Onest** (firmware & web UI font) | Fontsource subset | SIL OFL 1.1 | Copyright 2021 The Onest Project Authors |
| **Font Awesome 5 Free** (13 glyphs embedded in `ui/fonts/font_pixel_*.c`) | 5.x Free | SIL OFL 1.1 (font) / CC BY 4.0 (SVG) | Copyright (c) 2022 Fonticons, Inc. |
| **JetBrains Mono & IBM Plex Mono** (legacy `.woff` subsets in `assets/fonts/`, not linked in firmware) | Fontsource subsets | SIL OFL 1.1 | JetBrains s.r.o. / IBM Corp. |

---

## 1. MIT License — Pip-KeyPet, LVGL, Project Nayuki QR Code Generator, Three.js

### Pip-KeyPet
```text
MIT License

Copyright (c) 2026 David Novikov

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### LVGL 9.5.0
```text
MIT licence
Copyright (c) 2025 LVGL Kft

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```

### Project Nayuki QR Code Generator (in LVGL)
```text
Copyright © 2025 Project Nayuki. (MIT License)
https://www.nayuki.io/page/qr-code-generator-library

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

The Software is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and noninfringement. In no event shall the authors or copyright holders be liable for any claim, damages or other liability, whether in an action of contract, tort or otherwise, arising from, out of or in connection with the Software or the use or other dealings in the Software.
```

### Three.js (Web Simulator)
```text
The MIT License

Copyright © 2010-2024 three.js authors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```

---

## 2. Apache License 2.0 — ESP-IDF, Espressif Components, Waveshare BSP & Touch Driver, esptool-js, Material Symbols Rounded

Applies to:
- ESP-IDF (Espressif Systems)
- Espressif IDF Components (`button`, `cmake_utilities`, `esp_codec_dev`, `esp_io_expander`, `esp_lcd_co5300`, `esp_lcd_panel_io_additions`, `esp_lcd_touch`, `esp_lvgl_adapter`, `esp_lv_decoder`, `esp_lv_fs`, `esp_mmap_assets`, `knob`)
- Waveshare BSP (`waveshare/esp32_s3_touch_amoled_1_75c`) and Touch Driver (`waveshare/esp_lcd_touch_cst9217`)
- `esptool-js` (Espressif Systems)
- Material Symbols Rounded (Google LLC)

```text
                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

   1. Definitions.

      "License" shall mean the terms and conditions for use, reproduction,
      and distribution as defined by Sections 1 through 9 of this document.

      "Licensor" shall mean the copyright owner or entity authorized by
      the copyright owner that is granting the License.

      "Legal Entity" shall mean the union of the acting entity and all
      other entities that control, are controlled by, or are under common
      control with that entity. For the purposes of this definition,
      "control" means (i) the power, direct or indirect, to cause the
      direction or management of such entity, whether by contract or
      otherwise, or (ii) ownership of fifty percent (50%) or more of the
      outstanding shares, or (iii) beneficial ownership of such entity.

      "You" (or "Your") shall mean an individual or Legal Entity
      exercising permissions granted by this License.

      "Source" form shall mean the preferred form for making modifications,
      including but not limited to software source code, documentation
      source, and configuration files.

      "Object" form shall mean any form resulting from mechanical
      transformation or translation of a Source form, including but
      not limited to compiled object code, generated documentation,
      and conversions to other media types.

      "Work" shall mean the work of authorship, whether in Source or
      Object form, made available under the License, as indicated by a
      copyright notice that is included in or attached to the work
      (an example is provided in the Appendix below).

      "Derivative Works" shall mean any work, whether in Source or Object
      form, that is based on (or derived from) the Work and for which the
      editorial revisions, annotations, elaborations, or other modifications
      represent, as a whole, an original work of authorship. For the purposes
      of this License, Derivative Works shall not include works that remain
      separable from, or merely link (or bind by name) to the interfaces of,
      the Work and Derivative Works thereof.

      "Contribution" shall mean any work of authorship, including
      the original version of the Work and any modifications or additions
      to that Work or Derivative Works thereof, that is intentionally
      submitted to Licensor for inclusion in the Work by the copyright owner
      or by an individual or Legal Entity authorized to submit on behalf of
      the copyright owner. For the purposes of this definition, "submitted"
      means any form of electronic, verbal, or written communication sent
      to the Licensor or its representatives, including but not limited to
      communication on electronic mailing lists, source code control systems,
      and issue tracking systems that are managed by, or on behalf of, the
      Licensor for the purpose of discussing and improving the Work, but
      excluding communication that is conspicuously marked or otherwise
      designated in writing by the copyright owner as "Not a Contribution."

      "Contributor" shall mean Licensor and any individual or Legal Entity
      on behalf of whom a Contribution has been received by Licensor and
      subsequently incorporated within the Work.

   2. Grant of Copyright License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      copyright license to reproduce, prepare Derivative Works of,
      publicly display, publicly perform, sublicense, and distribute the
      Work and such Derivative Works in Source or Object form.

   3. Grant of Patent License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      (except as stated in this section) patent license to make, have made,
      use, offer to sell, sell, import, and otherwise transfer the Work,
      where such license applies only to those patent claims licensable
      by such Contributor that are necessarily infringed by their
      Contribution(s) alone or by combination of their Contribution(s)
      with the Work to which such Contribution(s) was submitted. If You
      institute patent litigation against any entity (including a
      cross-claim or counterclaim in a lawsuit) alleging that the Work
      or a Contribution incorporated within the Work constitutes direct
      or contributory patent infringement, then any patent licenses
      granted to You under this License for that Work shall terminate
      as of the date such litigation is filed.

   4. Redistribution. You may reproduce and distribute copies of the
      Work or Derivative Works thereof in any medium, with or without
      modifications, and in Source or Object form, provided that You
      meet the following conditions:

      (a) You must give any other recipients of the Work or
          Derivative Works a copy of this License; and

      (b) You must cause any modified files to carry prominent notices
          stating that You changed the files; and

      (c) You must retain, in the Source form of any Derivative Works
          that You distribute, all copyright, patent, trademark, and
          attribution notices from the Source form of the Work,
          excluding those notices that do not pertain to any part of
          the Derivative Works; and

      (d) If the Work includes a "NOTICE" text file as part of its
          distribution, then any Derivative Works that You distribute must
          include a readable copy of the attribution notices contained
          within such NOTICE file, excluding those notices that do not
          pertain to any part of the Derivative Works, in at least one
          of the following places: within a NOTICE text file distributed
          as part of the Derivative Works; within the Source form or
          documentation, if provided along with the Derivative Works; or,
          within a display generated by the Derivative Works, if and
          wherever such third-party notices normally appear. The contents
          of the NOTICE file are for informational purposes only and
          do not modify the License. You may add Your own attribution
          notices within Derivative Works that You distribute, alongside
          or as an addendum to the NOTICE text from the Work, provided
          that such additional attribution notices cannot be construed
          as modifying the License.

      You may add Your own copyright statement to Your modifications and
      may provide additional or different license terms and conditions
      for use, reproduction, or distribution of Your modifications, or
      for any such Derivative Works as a whole, provided Your use,
      reproduction, and distribution of the Work otherwise complies with
      the conditions stated in this License.

   5. Submission of Contributions. Unless You explicitly state otherwise,
      any Contribution intentionally submitted for inclusion in the Work
      by You to the Licensor shall be under the terms and conditions of
      this License, without any additional terms or conditions.
      Notwithstanding the above, nothing herein shall supersede or modify
      the terms of any separate license agreement you may have executed
      with Licensor regarding such Contributions.

   6. Trademarks. This License does not grant permission to use the trade
      names, trademarks, service marks, or product names of the Licensor,
      except as required for reasonable and customary use in describing the
      origin of the Work and reproducing the content of the NOTICE file.

   7. Disclaimer of Warranty. Unless required by applicable law or
      agreed to in writing, Licensor provides the Work (and each
      Contributor provides its Contributions) on an "AS IS" BASIS,
      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
      implied, including, without limitation, any warranties or conditions
      of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
      PARTICULAR PURPOSE. You are solely responsible for determining the
      appropriateness of using or redistributing the Work and assume any
      risks associated with Your exercise of permissions under this License.

   8. Limitation of Liability. In no event and under no legal theory,
      whether in tort (including negligence), contract, or otherwise,
      unless required by applicable law (such as deliberate and grossly
      negligent acts) or agreed to in writing, shall any Contributor be
      liable to You for damages, including any direct, indirect, special,
      incidental, or consequential damages of any character arising as a
      result of this License or out of the use or inability to use the
      Work (including but not limited to damages for loss of goodwill,
      work stoppage, computer failure or malfunction, or any and all
      other commercial damages or losses), even if such Contributor
      has been advised of the possibility of such damages.

   9. Accepting Warranty or Additional Liability. While redistributing
      the Work or Derivative Works thereof, You may choose to offer,
      and charge a fee for, acceptance of support, warranty, indemnity,
      or other liability obligations and/or rights consistent with this
      License. However, in accepting such obligations, You may act only
      on Your own behalf and on Your sole responsibility, not on behalf
      of any other Contributor, and only if You agree to indemnify,
      defend, and hold each Contributor harmless for any liability
      incurred by, or claims asserted against, such Contributor by reason
      of your accepting any such warranty or additional liability.

   END OF TERMS AND CONDITIONS
```

---

## 3. ESPRESSIF MIT License — `espressif/esp_new_jpeg` (1.0.2)

```text
 ESPRESSIF MIT License

 Copyright (c) 2024 <ESPRESSIF SYSTEMS (SHANGHAI) CO.，LTD>

 Permission is hereby granted for use on all ESPRESSIF SYSTEMS products, in which case,
 it is free of charge, to any person obtaining a copy of this software and associated
 documentation files (the "Software"), to deal in the Software without restriction, including
 without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
 and/or sell copies of the Software, and to permit persons to whom the Software is furnished
 to do so, subject to the following conditions:

 The above copyright notice and this permission notice shall be included in all copies or
 substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
 FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
 COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
 IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```

---

## 4. The FreeType Project License (FTL) — `espressif/freetype` (2.14.3)

Used under the FreeType License (FTL).

```text
                    The FreeType Project LICENSE
                    ----------------------------

                            2006-Jan-27

                    Copyright 1996-2002, 2006 by
          David Turner, Robert Wilhelm, and Werner Lemberg

  Portions of this software are copyright © 2026 The FreeType
  Project (https://freetype.org). All rights reserved.

0. Definitions
  Throughout this license, the terms `package', `FreeType Project',
  and `FreeType archive' refer to the set of files originally
  distributed by the authors (David Turner, Robert Wilhelm, and
  Werner Lemberg) as the `FreeType Project', be they named as alpha,
  beta or final release.

  `You' refers to the licensee, or person using the project, where
  `using' is a generic term including compiling the project's source
  code as well as linking it to form a `program' or `executable'.
  This program is referred to as `a program using the FreeType
  engine'.

  This license applies to all files distributed in the original
  FreeType Project, including all source code, binaries and
  documentation, unless otherwise stated in the file in its
  original, unmodified form as distributed in the original archive.

  The FreeType Project is copyright (C) 1996-2000 by David Turner,
  Robert Wilhelm, and Werner Lemberg. All rights reserved except as
  specified below.

1. No Warranty
  THE FREETYPE PROJECT IS PROVIDED `AS IS' WITHOUT WARRANTY OF ANY
  KIND, EITHER EXPRESS OR IMPLIED, INCLUDING, BUT NOT LIMITED TO,
  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
  PURPOSE. IN NO EVENT WILL ANY OF THE AUTHORS OR COPYRIGHT HOLDERS
  BE LIABLE FOR ANY DAMAGES CAUSED BY THE USE OR THE INABILITY TO
  USE, OF THE FREETYPE PROJECT.

2. Redistribution
  This license grants a worldwide, royalty-free, perpetual and
  irrevocable right and license to use, execute, perform, compile,
  display, copy, create derivative works of, distribute and
  sublicense the FreeType Project (in both source and object code
  forms) and derivative works thereof for any purpose; and to
  authorize others to exercise some or all of the rights granted
  herein, subject to the following conditions:

    o Redistribution of source code must retain this license file
      (`FTL.TXT') unaltered; any additions, deletions or changes to
      the original files must be clearly indicated in accompanying
      documentation. The copyright notices of the unaltered,
      original files must be preserved in all copies of source
      files.

    o Redistribution in binary form must provide a disclaimer that
      states that the software is based in part of the work of the
      FreeType Team, in the distribution documentation. We also
      encourage you to put an URL to the FreeType web page in your
      documentation, though this isn't mandatory.

  These conditions apply to any software derived from or based on
  the FreeType Project, not just the unmodified files. If you use
  our work, you must acknowledge us. However, no fee need be paid
  to us.

3. Advertising
  Neither the FreeType authors and contributors nor you shall use
  the name of the other for commercial, advertising, or promotional
  purposes without specific prior written permission.
```

---

## 5. PNG Reference Library License v2 — `espressif/libpng` (1.6.58)

```text
PNG Reference Library License version 2
---------------------------------------

 * Copyright (c) 1995-2019 The PNG Reference Library Authors.
 * Copyright (c) 2018-2019 Cosmin Truta.
 * Copyright (c) 2000-2002, 2004, 2006-2018 Glenn Randers-Pehrson.
 * Copyright (c) 1996-1997 Andreas Dilger.
 * Copyright (c) 1995-1996 Guy Eric Schalnat, Group 42, Inc.

The software is supplied "as is", without warranty of any kind,
express or implied, including, without limitation, the warranties
of merchantability, fitness for a particular purpose, title, and
non-infringement. In no event shall the Copyright owners, or
anyone distributing the software, be liable for any damages or
other liability, whether in contract, tort or otherwise, arising
from, out of, or in connection with the software, or the use or
other dealings in the software, even if advised of the possibility
of such damage.

Permission is hereby granted to use, copy, modify, and distribute
this software, or portions hereof, for any purpose, without fee,
subject to the following restrictions:

 1. The origin of this software must not be misrepresented; you
    must not claim that you wrote the original software. If you
    use this software in a product, an acknowledgment in the product
    documentation would be appreciated, but is not required.

 2. Altered source versions must be plainly marked as such, and must
    not be misrepresented as being the original software.

 3. This Copyright notice may not be removed or altered from any
    source or altered source distribution.
```

---

## 6. Zlib License — `espressif/zlib` (1.3.2)

```text
Copyright notice:

 (C) 1995-2022 Jean-loup Gailly and Mark Adler

  This software is provided 'as-is', without any express or implied
  warranty. In no event will the authors be held liable for any damages
  arising from the use of this software.

  Permission is granted to anyone to use this software for any purpose,
  including commercial applications, and to alter it and redistribute it
  freely, subject to the following restrictions:

  1. The origin of this software must not be misrepresented; you must not
     claim that you wrote the original software. If you use this software
     in a product, an acknowledgment in the product documentation would be
     appreciated but is not required.
  2. Altered source versions must be plainly marked as such, and must not
     be misrepresented as being the original software.
  3. This notice may not be removed or altered from any source distribution.
```

---

## 7. SIL Open Font License 1.1 — Onest, Font Awesome 5 Free (and legacy JetBrains Mono / IBM Plex Mono)

Applies to:
- **Onest** — Copyright 2021 The Onest Project Authors (<https://github.com/simpals/onest>)
- **Font Awesome 5 Free** (13 glyphs embedded in `ui/fonts/font_pixel_*.c`) — Copyright (c) 2022 Fonticons, Inc. (<https://fontawesome.com>), with Reserved Font Name: `"Font Awesome"`. (Font files under SIL OFL 1.1; SVG/JS icons under CC BY 4.0.)
- **JetBrains Mono** — Copyright 2020 The JetBrains Mono Project Authors (`assets/fonts/`, not linked into firmware)
- **IBM Plex Mono** — Copyright © 2017 IBM Corp. (`assets/fonts/`, not linked into firmware)

```text
SIL OPEN FONT LICENSE
Version 1.1 - 26 February 2007

PREAMBLE
The goals of the Open Font License (OFL) are to stimulate worldwide
development of collaborative font projects, to support the font creation
efforts of academic and linguistic communities, and to provide a free and
open framework in which fonts may be shared and improved in partnership
with others.

The OFL allows the licensed fonts to be used, studied, modified and
redistributed freely as long as they are not sold by themselves. The
fonts, including any derivative works, can be bundled, embedded,
redistributed and/or sold with any software provided that any reserved
names are not used by derivative works. The fonts and derivatives,
however, cannot be released under any other type of license. The
requirement for fonts to remain under this license does not apply
to any document created using the fonts or their derivatives.

DEFINITIONS
"Font Software" refers to the set of files released by the Copyright
Holder(s) under this license and clearly marked as such. This may
include source files, build scripts and documentation.

"Reserved Font Name" refers to any names specified as such after the
copyright statement(s).

"Original Version" refers to the collection of Font Software components as
distributed by the Copyright Holder(s).

"Modified Version" refers to any derivative made by adding to, deleting,
or substituting — in part or in whole — any of the components of the
Original Version, by changing formats or by porting the Font Software to a
new environment.

"Author" refers to any designer, engineer, programmer, technical
writer or other person who contributed to the Font Software.

PERMISSION & CONDITIONS
Permission is hereby granted, free of charge, to any person obtaining
a copy of the Font Software, to use, study, copy, merge, embed, modify,
redistribute, and sell modified and unmodified copies of the Font
Software, subject to the following conditions:

1) Neither the Font Software nor any of its individual components,
in Original or Modified Versions, may be sold by itself.

2) Original or Modified Versions of the Font Software may be bundled,
redistributed and/or sold with any software, provided that each copy
contains the above copyright notice and this license. These can be
included either as stand-alone text files, human-readable headers or
in the appropriate machine-readable metadata fields within text or
binary files as long as those fields can be easily viewed by the user.

3) No Modified Version of the Font Software may use the Reserved Font
Name(s) unless explicit written permission is granted by the corresponding
Copyright Holder. This restriction only applies to the primary font name as
presented to the users.

4) The name(s) of the Copyright Holder(s) or the Author(s) of the Font
Software shall not be used to promote, endorse or advertise any
Modified Version, except to acknowledge the contribution(s) of the
Copyright Holder(s) and the Author(s) or with their explicit written
permission.

5) The Font Software, modified or unmodified, in part or in whole,
must be distributed entirely under this license, and must not be
distributed under any other license. The requirement for fonts to
remain under this license does not apply to any document created
using the fonts or their derivatives.

TERMINATION
This license becomes null and void if any of the above conditions are
not met.

DISCLAIMER
THE FONT SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT
OF COPYRIGHT, PATENT, TRADEMARK, OR OTHER RIGHT. IN NO EVENT SHALL THE
COPYRIGHT HOLDER BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
INCLUDING ANY GENERAL, SPECIAL, INDIRECT, INCIDENTAL, OR CONSEQUENTIAL
DAMAGES, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
```
