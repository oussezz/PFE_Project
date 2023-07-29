import json

# Load trainer_state.json
with open("E:/Weights (pfe+master)/google_vit_base_patch16_224_in21k__lt_1e-05/checkpoint-246000/trainer_state.json", "r") as f:
    trainer_state = json.load(f)
import matplotlib.pyplot as plt
# Extract eval_accuracy values
eval_acc_list = [0]
epoch_list = [0]
for eval_result in trainer_state["log_history"]:
    if "eval_accuracy" in eval_result and "epoch" in eval_result:
        eval_acc_list.append(eval_result["eval_accuracy"])
        epoch_list.append(eval_result["epoch"])

# Plot evaluation accuracy over epochs
plt.plot(epoch_list, eval_acc_list, marker=None)
plt.title("Précision par époque du modèle 'Facebook/DeiT-base-patch16-224'")
plt.xlabel("époque")
plt.ylabel("Précision")

plt.savefig('google_vit_base_patch16_224_in21k__lt_1e-05.png')

plt.show()
#save plot