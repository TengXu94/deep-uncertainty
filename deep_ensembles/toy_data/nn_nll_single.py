import torch
from deep_ensembles.models.gaussian_mlp import GaussianMLP
from deep_ensembles.params.TrainingParameters import TrainingParameters
from deep_ensembles.toy_data.data_generator import generate_data
from losses.nll import NLLloss
from plotting.Plotter import Plotter

if __name__ == "__main__":
    plotter = Plotter()
    noisy_points_x, noisy_points_y, x, y = generate_data(
        points=20, xrange=(-4, 4), std=3.0
    )
    gmlp = GaussianMLP(hidden_layers=[100])
    gmlp_optimizer = torch.optim.Adam(
        params=gmlp.parameters(), lr=TrainingParameters.learning_rate
    )

    for epoch in range(TrainingParameters.epochs):
        gmlp_optimizer.zero_grad()
        mean, var = gmlp(noisy_points_x)
        gmlp_loss = NLLloss(noisy_points_y, mean, var)  # NLL loss

        if epoch == 0:
            print("initial loss: ", gmlp_loss.item())
        gmlp_loss.backward()
        gmlp_optimizer.step()
    print("final loss: ", gmlp_loss.item())

    mean, var = gmlp(torch.tensor(x).float())

    plotter.plot_deep_ensemble_toy_data(
        noisy_points_x=noisy_points_x.numpy(),
        nosy_points_y=noisy_points_y.numpy(),
        ground_truth_x=x,
        ground_truth_y=y,
        prediction_mean=mean.detach().numpy(),
        prediction_variance=var.detach().numpy(),
        label="GMLP NLL",
        title="Second Figure",
        file_name="deep_ensembles/plots/toy_data/nll_single.png",
    )
