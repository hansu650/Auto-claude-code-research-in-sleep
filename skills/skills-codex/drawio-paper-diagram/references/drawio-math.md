# Draw.io MathJax Rules

Use true MathJax for all mathematical variables, operators, dimensions, sets, and equations.

## Required model setting

Set `math="1"` on the relevant `mxGraphModel`:

```xml
<mxGraphModel math="1" ...>
```

## Label forms

Use inline math for labels:

```text
\(i+1\)
```

Use display math only for a standalone equation:

```text
\[\mathbf{p}_w=\frac{1}{3}\sum_s\mathbf{p}_{w,s}\]
```

Escape XML characters when editing raw XML.

## Conversions

| Plain or fake label | MathJax label |
|---|---|
| `i + 1` | `\(i+1\)` |
| `Σ/3` | `\(\frac{1}{3}\sum_s\)` |
| `p<sub>w</sub>` | `\(p_w\)` |
| `14 x 14` | `\(14\times14\)` |
| `[1,1,0]` | `\(\left[1,1,0\right]\)` |
| `R+^196` | `\(\mathbb{R}^{196}_{+}\)` |

Do not use ordinary Arial text, HTML `<sub>`/`<sup>`, or a Unicode operator to imitate mathematical typesetting.

## Keep normal text normal

Do not wrap these in MathJax:

- method names such as IHP, NCTP, and ViTTrace;
- ordinary English labels such as Input, Encoder, and Output;
- subfigure markers such as `(a)` and `(b)`.

For mixed labels, separate the prose and math when possible, for example a normal `Fused patch field` label above a MathJax `\(\mathbf{p}_w\in\mathbb{R}^{196}_{+}\)` label.

## Placement

- Put an equation next to the operation or object it explains.
- Keep input and output quantities visible.
- Avoid placing several unrelated equations inside one large box.
- Use a worked local example so symbols and visible objects correspond one-to-one.

## Export check

After export, zoom into the PDF and confirm that variables are italic and subscripts, fractions, and operators use a mathematics font such as STIX or Computer Modern. Confirm that the output remains vector.
