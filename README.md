# UPEval

**UPEval** is a user-perspective evaluation framework for **Emotional Support Conversations (ESC)**.  
It evaluates **over-empathy** in multi-turn ESC — such as patterned responses and strategy overuse — by combining:

- a **role-based user simulator**, and  
- **open-ended, user-centered feedback scoring model**.



## 📁 Repository Structure

```text
UPEval/
├── data_for_UPEval/
│   ├── 200_AugESC_for_evalframe_wrole.json
│   └── 200_ESConv_for_evalframe_wrole.json
├── prompts/
│   └── gen.jinja
└── scripts/
    ├── run_sh.sh
    ├── main.py
    ├── minutes_writer.py
    ├── prompt_template.py
    ├── tasks.py
    ├── utils.py
    └── README.md  
   ```

## 📚 Data Description (`data_for_UPEval/`)

-   **200_ESConv_for_evalframe_wrole.json**
    
-   **200_AugESC_for_evalframe_wrole.json**
    

These are **200-dialogue subsets** from ESConv and AugESC ([download](https://drive.google.com/drive/folders/1jc7DDSuMkx1EKVpKyu_YY1F8UfBmK9KU?usp=drive_link)).  
They include **role-annotated** help-seeker/supporter turns and are used to run UPEval experiments as described in the paper.

## 🧩 Prompts (`prompts/`)

-   **gen.jinja**  
    Jinja template containing:
    
    -   user simulator role prompts
        
    -   supporter model prompts
        
    -   evaluator prompts that convert **open-ended feedback → 1–5 strategy scores**  
        (strategies include Q, RP, RF, SD, AR, PS, INF, plus dialogue-level repetitiveness)
        



## ▶️ Run

### 1. Environment setup

`conda create -n upeval python=3.10`
`conda activate upeval`
`pip install -r requirements.txt `

### 2. Run evaluation

Using shell script:

`cd scripts
bash run_sh.sh` 


This will execute:

1.  Multi-turn ESC interaction
    
2.  User-centered feedback generation
    
3.  Strategy-level scoring
    
4.  Dialogue-level repetitiveness scoring
    
5.  Logging to output files
    





## 📬 Contact

If you have questions about the implementation or the paper, please contact:  
**Suhyune Son** — ssh5131@korea.ac.kr


