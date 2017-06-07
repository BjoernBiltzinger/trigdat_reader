from threeML.plugins.DispersionSpectrumLike import DispersionSpectrumLike
from astromodels.functions.priors import Uniform_prior, Cosine_Prior


class BALROGLike(DispersionSpectrumLike):
    def __init__(self,
                 name,
                 observation,
                 background=None,
                 time=0,
                 free_position=True,
                 verbose=True):
        """
        BALROGLike is a general plugin for fitting GBM spectra and locations at the same time



        :param name: plugin name
        :param observation: observed spectrum
        :param background: background spectrum
        :param time: time of the observation
        :param free_position: keep the position free
        :param verbose: the verbosity level of the plugin
        """

        self._free_position = free_position

        super(BALROGLike, self).__init__(name, observation, background,
                                         verbose)

        # only on the start up
        self._rsp.set_time(time)

    def set_model(self, likelihoodModel):
        """
        Set the model and free the location parameters


        :param likelihoodModel:
        :return:
        """

        # set the standard likelihood model

        super(BALROGLike, self).set_model(likelihoodModel)

        # now free the position

        if self._free_position:

            if self._verbose:
                print('Freeing the position and setting priors')

            for key in self._like_model.point_sources.keys():
                self._like_model.point_sources[key].position.ra.free = True
                self._like_model.point_sources[key].position.dec.free = True

                self._like_model.point_sources[
                    key].position.ra.prior = Uniform_prior(
                    lower_bound=0., upper_bound=360)
                self._like_model.point_sources[
                    key].position.dec.prior = Cosine_Prior(
                    lower_bound=-90., upper_bound=90)


                ra = self._like_model.point_sources[key].position.ra.value
                dec = self._like_model.point_sources[key].position.dec.value

        

            
            self._rsp.set_location(ra, dec)



                

    def get_model(self):

        # Here we update the GBM drm parameters which creates and new DRM for that location
        # we should only be dealing with one source for GBM

        # if not self._is_rsp_set:

        for key in self._like_model.point_sources.keys():
            ra = self._like_model.point_sources[key].position.ra.value
            dec = self._like_model.point_sources[key].position.dec.value

        # update the location

        if self._free_position:
            self._rsp.set_location(ra, dec)

        return super(BALROGLike, self).get_model()

    @classmethod
    def from_spectrumlike(cls, spectrum_like, time, free_position=True):

        return cls(spectrum_like.name, spectrum_like._observed_spectrum,
                   spectrum_like._background_spectrum, time, free_position,
                   spectrum_like._verbose)
