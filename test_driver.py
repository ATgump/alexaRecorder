from xml.etree.ElementPath import find
import find_marker

#find_marker.pad(clip="C:\\Users\\avery\\OneDrive\\Desktop\\test\\testing_tones\\ae_MSE_trial_1_candidate_0.wav",padding="C:\\Users\\avery\\OneDrive\\Desktop\\3000hz_p08_amp_p5_time.wav",export_path="C:\\Users\\avery\\OneDrive\\Desktop\\test\\test_tones_padded\\ae_MSE_trial_1_candidate_0.wav")

ta,md,ma = find_marker.trim_time("C:\\Users\\avery\\OneDrive\\Desktop\\test\\test_tones_padded\\ae_MSE_trial_1_candidate_0.wav")

print(ta)
print(md)
print(ma)